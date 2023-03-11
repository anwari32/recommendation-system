from typing import Union
from fastapi import FastAPI, Depends, HTTPException
import pickle
import os
import scann
import pandas as pd
import numpy as np

from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

from sklearn.linear_model import LinearRegression

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_root():
    return {"Hello": "World"}


@app.post("/category/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    # db_cat = crud.get_category_by_name(db, category.name)
    # if db_cat:
    #     raise HTTPException(status_code=400, detail=f"Category '{db_cat.name}' has been registered.")
    return crud.create_category(db=db, category=category)


@app.post("/courier/", response_model=schemas.Courier)
def create_courier(courier: schemas.CourierCreate, db: Session = Depends(get_db)):
    # db_courier = crud.get_courier_by_name(db, courier.name)
    # if db_courier:
    #     raise HTTPException(status_code=400, detail=f"Courier '{db_courier.name}' has been registered.")
    return crud.create_courier(db=db, courier=courier)

# @app.get("/category/{cat_id}", response_model=schemas.Category)
# def get_category_by_id(cat_id: int, db: Session = Depends(get_db)):
#     db_cat = crud.get_category_by_id(db, cat_id)
#     return {"id": cat_id, "name": db_cat.name}


@app.get("/recommend")
def recommend(item_id, price, qty, courier_id, insurance, db: Session = Depends(get_db)):
    query_object = {
        "item_id": item_id,
        "price": price,
        "quantity": qty,
        "courier_id": courier_id,
        "use_insurance": insurance
    }
    print(query_object)

    # find detail about this item
    db_item = crud.get_item_by_id(db, item_id)
    cat_id = None
    if db_item:
        cat_id = db_item.cat_id
    print(f"cat_id {cat_id}")

    # filter session based on existing category id.
    # if category is None, get latest sessions.
    LATEST_SESSIONS_LIMIT = 100000
    db_sessions = []
    if cat_id:
        db_sessions = crud.get_session_by_item_cat_id(db, cat_id)
    else:
        db_sessions = crud.get_session(db, skip=0, limit=LATEST_SESSIONS_LIMIT)

    _columns = ["id", "session_ref_id", "item_id", "price_per_qty", "qty", "courier_id", "insurance"]
    entries = []
    for s in db_sessions:
        _price_per_qty = 0 if s.price == 0 or s.qty == 0 else s.price_per_qty
        _insurance = 1 if bool(s.insurance) else 0
        entries.append(
            [s.id, s.session_ref_id, s.item_id, _price_per_qty, s.qty, s.courier_id, _insurance]
        )
    dataframe = pd.DataFrame(entries, columns=_columns)
    # dataframe.to_csv("_temp_csv", index=False)

    # init scann instance
    features = ["price_per_qty", "qty", "courier_id", "insurance"]
    training_vectors = dataframe[features]

    scann_instance = scann.scann_ops_pybind.builder(training_vectors, 10, "dot_product").tree(
        num_leaves=10, num_leaves_to_search=100, training_sample_size=250000).score_ah(
        2, anisotropic_quantization_threshold=0.2).reorder(100).build()

    # search candidates.
    query = [int(price) / int(qty), int(qty), int(courier_id), int(insurance)]
    query = np.asarray(query)
    neighbors, distances = scann_instance.search(query)

    # generate regression linear model.
    X_train = training_vectors
    y_train = [1] * dataframe.shape[0]

    linearReg = LinearRegression()
    reg = linearReg.fit(X_train, y_train)

    # compute regression linear value.
    X_test = training_vectors.loc[neighbors[0], features]
    X_test = [X_test]
    y_test = reg.predict(X_test)
    min_score = np.min(y_test)
    min_index = np.argmin(y_test)

    p = dataframe.loc[min_index, :]
    col_index = dataframe.columns.get_loc("item_id")
    courier_index = dataframe.columns.get_loc("courier_id")
    item_id = p.tolist()[2]
    return {
        "regression_score": min_score,
        "item_id": str(int(item_id)),
        "courier_id": str(courier_index)
    }