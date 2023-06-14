# Databricks notebook source
# DBTITLE 1,Create CATALOG if does not exist
# MAGIC %sql
# MAGIC CREATE CATALOG  IF NOT EXISTS mlops_pj

# COMMAND ----------

# DBTITLE 1,Create Database if does not exist
# MAGIC %sql
# MAGIC USE CATALOG mlops_pj;
# MAGIC CREATE DATABASE IF NOT EXISTS transaction_raw 

# COMMAND ----------

# DBTITLE 1,Create Raw files as save as table
import os
import numpy as np
import pandas as pd
df = spark.read.option("inferSchema", "true") \
          .option("header", "true") \
          .option("delim", ",") \
          .csv(f"file:///{os.getcwd()}/fraud_raw.csv") 

# COMMAND ----------

df = df.drop('AUTH_ID')
df = df.withColumnRenamed('AUTH_ID_new', 'AUTH_ID')
df.write \
  .format("delta") \
  .mode("overwrite") \
  .option("overwriteSchema", "true") \
  .saveAsTable("transaction_raw.transaction")

# COMMAND ----------

display(spark.read.table("transaction_raw.transaction"))

# COMMAND ----------

# MAGIC %md
# MAGIC # Mock New Data

# COMMAND ----------


df =spark.read.table("transaction_raw.transaction")
df = df.toPandas()
df = df[1800:1904]

# COMMAND ----------

for col in ['ACCT_PROD_CD','ACCT_AVL_CASH_BEFORE_AMT','ACCT_AVL_MONEY_BEFORE_AMT','ACCT_CL_AMT','APPRD_AUTHZN_CNT','APPRD_AUTHZN_CNT']:
  df[col] = df[col].mean() +np.random.default_rng().choice(10, size=(df.shape[0]))

# Randomize the fraud indicator
df["FRD_IND"] = np.random.default_rng().choice([0,1], size=(df.shape[0]))
df['AUTH_ID'] = df['AUTH_ID'] +500

# COMMAND ----------

display(df)

# COMMAND ----------

# df=spark.createDataFrame(df) 
df.write \
  .format("delta") \
  .mode("append") \
  .option("overwriteSchema", "true") \
  .saveAsTable("transaction_raw.transaction")

# COMMAND ----------


