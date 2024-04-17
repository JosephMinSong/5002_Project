from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from sys import argv

# Capture the filename from command-line arguments
filename = argv[1]

# Start Spark session
spark = SparkSession.builder.appName("LogisticRegressionExample").getOrCreate()

# Load data
data = spark.read.csv(filename, inferSchema=True, header=True)

# Select features and label
# data = data.select('feature1', 'feature2', ..., 'label')

# VectorAssembler to combine feature columns into a single vector column
assembler = VectorAssembler(
    inputCols=["feature1", "feature2", ...], outputCol="features"
)
data = assembler.transform(data)

# Split data into training and test sets
train_data, test_data = data.randomSplit([0.7, 0.3], seed=42)

# Create and train the model
lr = LogisticRegression(featuresCol="features", labelCol="label")
lr_model = lr.fit(train_data)

# Predict and evaluate the model
predictions = lr_model.transform(test_data)
evaluator = BinaryClassificationEvaluator(
    rawPredictionCol="rawPrediction", labelCol="label"
)
accuracy = evaluator.evaluate(predictions)

print(f"Test Accuracy: {accuracy}")

# Stop Spark session
spark.stop()
