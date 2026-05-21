import json
from pathlib import Path


CATEGORIES = {
    "Python for ML": [
        ("Why are list comprehensions often used in ML preprocessing?", "They create transformed lists concisely and readably", "They automatically train models", "They replace NumPy arrays", "They encrypt datasets", "option1", "List comprehensions are a compact Python pattern for transforming and filtering data before it enters a model."),
        ("What does a Python virtual environment isolate?", "Project dependencies", "GPU temperature", "CSV delimiters", "Database indexes", "option1", "Virtual environments keep package versions scoped to one project, which helps reproducible ML work."),
        ("Which Python object is commonly used for key-value feature metadata?", "dict", "tuple only", "set only", "bytes", "option1", "Dictionaries map names to values and are useful for configs, metrics, and feature metadata."),
        ("What is the purpose of a generator in data pipelines?", "Yield data lazily", "Sort labels automatically", "Increase target leakage", "Disable batching", "option1", "Generators can stream samples without loading an entire dataset into memory."),
        ("What does pickle commonly store in ML projects?", "Serialized Python objects", "Only SQL tables", "Only image pixels", "Terminal logs", "option1", "Pickle can serialize fitted preprocessors or models, though safer formats are preferred for untrusted files."),
    ],
    "NumPy": [
        ("What does NumPy broadcasting allow?", "Operations on compatible different-shaped arrays", "Training without data", "Automatic model deployment", "Text tokenization only", "option1", "Broadcasting expands compatible dimensions logically so vectorized operations can run without manual loops."),
        ("What is a NumPy ndarray?", "A multidimensional homogeneous array", "A SQL cursor", "A Flask route", "A GPU driver", "option1", "ndarray is NumPy's core structure for fast numerical computing."),
        ("Why prefer vectorized NumPy operations?", "They use optimized low-level loops", "They remove the need for validation", "They always reduce bias", "They create labels", "option1", "Vectorized operations are typically faster and clearer than Python loops for array math."),
        ("What does axis=0 usually refer to in a 2D array?", "Column-wise aggregation down rows", "Row-wise aggregation across columns", "The random seed", "The model output layer", "option1", "For many NumPy reductions, axis=0 collapses rows and returns one value per column."),
        ("What does np.random.seed help with?", "Reproducible random results", "Higher accuracy by itself", "Database security", "HTML rendering", "option1", "Setting a seed makes pseudo-random operations repeatable during experiments."),
    ],
    "Pandas": [
        ("What is a Pandas DataFrame?", "A labeled 2D table", "A neural layer", "A loss function", "A shell command", "option1", "DataFrames store tabular data with row indexes and named columns."),
        ("What does df.groupby() support?", "Split-apply-combine aggregations", "GPU kernel compilation", "Password hashing", "Model serving only", "option1", "groupby separates rows by keys, applies calculations, and combines the results."),
        ("Why use df.isna().sum()?", "Count missing values per column", "Normalize every column", "Train a classifier", "Create embeddings", "option1", "It is a quick missingness audit before cleaning or imputing data."),
        ("What does one-hot encoding create?", "Binary columns for categories", "Encrypted feature names", "Only ordinal labels", "A validation split", "option1", "One-hot encoding represents categories as indicator columns for many ML algorithms."),
        ("What is a common risk when joining DataFrames?", "Duplicating rows through many-to-many keys", "Removing all variance always", "Changing Python version", "Forcing GPU use", "option1", "Unexpected key duplication can inflate datasets and distort training data."),
    ],
    "Data Science": [
        ("What is exploratory data analysis?", "Investigating structure, quality, and patterns", "Deploying a model to production", "Writing only CSS", "Encrypting features", "option1", "EDA helps understand distributions, missingness, relationships, and anomalies before modeling."),
        ("What is data leakage?", "Using information unavailable at prediction time", "A slow database", "A small batch size", "A missing import", "option1", "Leakage makes validation scores unrealistically high because the model sees future or target-derived information."),
        ("Why split train and test data?", "Estimate generalization on unseen data", "Make files smaller", "Avoid all preprocessing", "Remove labels", "option1", "A held-out set checks how well the model performs beyond the training examples."),
        ("What does a data dictionary describe?", "Feature meanings and allowed values", "Only model weights", "HTML classes", "Optimizer momentum", "option1", "Data dictionaries make datasets easier to audit, clean, and use correctly."),
        ("What is feature engineering?", "Creating useful model inputs from raw data", "Choosing a web font", "Deleting all outliers", "Hashing passwords", "option1", "Feature engineering transforms raw signals into representations that models can learn from."),
    ],
    "Statistics": [
        ("What does standard deviation measure?", "Spread around the mean", "Class label count only", "Model latency", "Token length only", "option1", "Standard deviation quantifies variability in a numeric distribution."),
        ("What is a p-value?", "Probability of data as extreme under a null hypothesis", "Probability the model is deployed", "Percentage of missing data", "Training accuracy", "option1", "A p-value measures how surprising the observed statistic is if the null hypothesis were true."),
        ("What does correlation measure?", "Strength and direction of association", "Causation automatically", "Model memory usage", "Feature encryption", "option1", "Correlation describes association but does not prove causality."),
        ("What is a confidence interval?", "A plausible range for a population parameter", "A hidden layer", "A database lock", "A JSON field", "option1", "Confidence intervals express estimation uncertainty from sampled data."),
        ("What is variance?", "Average squared deviation from the mean", "The mean itself", "A class name", "A deployment port", "option1", "Variance is a squared measure of how dispersed values are."),
    ],
    "Probability": [
        ("What is conditional probability?", "Probability of an event given another event", "Probability without data", "The number of classes", "The learning rate", "option1", "Conditional probability updates event likelihood when related information is known."),
        ("What does Bayes' theorem update?", "Beliefs using evidence", "Model weights without data", "HTML pages", "GPU memory", "option1", "Bayes' theorem connects prior belief, likelihood, and posterior belief."),
        ("What is an independent event?", "One event does not affect another's probability", "A feature with missing values", "A model without labels", "A row with duplicates", "option1", "Independence means knowing one event occurred does not change the probability of the other."),
        ("What is expected value?", "Long-run average outcome", "Maximum observed value", "Minimum loss only", "Number of epochs", "option1", "Expected value is a probability-weighted average of possible outcomes."),
        ("What does a probability distribution describe?", "Likelihoods of possible values", "Only file paths", "CSS colors", "API routes", "option1", "Distributions assign probabilities or densities across outcomes."),
    ],
    "Linear Algebra": [
        ("What is a vector in ML?", "An ordered list of numeric values", "A web route", "A password hash", "A SQL table only", "option1", "Vectors commonly represent samples, weights, gradients, or embeddings."),
        ("What does matrix multiplication combine?", "Rows and columns through dot products", "Only strings", "HTTP requests", "CSS selectors", "option1", "Matrix multiplication is central to linear models and neural network layers."),
        ("What is an eigenvector?", "A vector whose direction is unchanged by a linear transform", "A missing value", "A training loop", "A plot legend", "option1", "Eigenvectors reveal directions that a transformation scales without rotating."),
        ("What does the dot product measure?", "Alignment between two vectors", "File size", "Number of labels", "Batch count only", "option1", "The dot product is large when vectors point in similar directions and have large magnitudes."),
        ("Why are embeddings vectors?", "They encode items in continuous numeric space", "They are always images", "They replace validation", "They store passwords", "option1", "Embeddings place semantic or learned relationships into vector space."),
    ],
    "Machine Learning Basics": [
        ("What is overfitting?", "Learning noise instead of general patterns", "Having no features", "Using a database", "Deploying a model", "option1", "Overfit models perform well on training data but poorly on unseen data."),
        ("What is underfitting?", "A model too simple to capture patterns", "A model with too many logs", "A table join", "A CSS error", "option1", "Underfit models have high error because they miss important structure in the data."),
        ("What is a loss function?", "A measure of prediction error to optimize", "A database backup", "A chart color", "A login route", "option1", "Training algorithms minimize a loss function to improve predictions."),
        ("What is a validation set used for?", "Tuning model choices during development", "Final unbiased reporting only", "Password storage", "Image compression", "option1", "Validation data guides hyperparameter and model selection before final testing."),
        ("What is regularization?", "A penalty or constraint to reduce overfitting", "A data leak", "A UI animation", "A deployment log", "option1", "Regularization discourages overly complex models so they generalize better."),
    ],
    "Supervised Learning": [
        ("What defines supervised learning?", "Training with input-output examples", "Training without labels", "Only clustering", "Only compression", "option1", "Supervised models learn from examples paired with target labels or values."),
        ("What is classification?", "Predicting a discrete class", "Predicting only continuous values", "Sorting columns", "Creating CSS", "option1", "Classification maps inputs to categories such as spam or not spam."),
        ("What is regression?", "Predicting a continuous value", "Finding clusters only", "Tokenizing prompts", "Hashing passwords", "option1", "Regression estimates numeric targets such as price or demand."),
        ("What does a decision tree split on?", "Feature thresholds or category tests", "HTML elements", "Passwords", "Ports", "option1", "Trees partition data using feature-based rules to improve target purity."),
        ("What is cross-validation?", "Repeated train-validation splits", "A single final test only", "Database replication", "GPU cooling", "option1", "Cross-validation estimates performance across multiple folds for more stable evaluation."),
    ],
    "Unsupervised Learning": [
        ("What is clustering?", "Grouping similar unlabeled examples", "Predicting known labels", "Serving APIs", "Hashing data", "option1", "Clustering discovers structure when explicit labels are unavailable."),
        ("What does PCA do?", "Projects data onto high-variance directions", "Adds labels to rows", "Runs Flask", "Encrypts features", "option1", "PCA reduces dimensionality by finding orthogonal directions that explain variance."),
        ("What is anomaly detection?", "Finding unusual observations", "Always balancing classes", "Making dashboards", "Changing passwords", "option1", "Anomaly detection flags rare or suspicious patterns that differ from normal data."),
        ("What does k-means minimize?", "Within-cluster squared distances", "Cross entropy only", "HTTP latency", "Feature names", "option1", "K-means places centroids to reduce distances between points and assigned cluster centers."),
        ("What is dimensionality reduction useful for?", "Compression, visualization, and noise reduction", "Creating user sessions", "Removing all labels", "Increasing leakage", "option1", "Reducing dimensions can simplify data while retaining important structure."),
    ],
    "Deep Learning": [
        ("What is deep learning?", "Learning with multi-layer neural networks", "Only SQL analytics", "A CSS framework", "Manual rules only", "option1", "Deep learning uses layered neural networks to learn representations from data."),
        ("What is backpropagation?", "Computing gradients through a network", "Backing up a database", "Sorting rows", "Deploying prompts", "option1", "Backpropagation applies the chain rule to compute parameter gradients efficiently."),
        ("What is an activation function?", "A nonlinear transformation in a neural layer", "A database trigger", "A password policy", "A CSV delimiter", "option1", "Activations let neural networks model nonlinear relationships."),
        ("What is dropout?", "Randomly disabling units during training", "Deleting the dataset", "Skipping validation", "Removing labels", "option1", "Dropout regularizes neural networks by reducing co-adaptation of units."),
        ("What is a learning rate?", "Step size for optimizer updates", "Number of features", "Class balance", "HTTP timeout", "option1", "The learning rate controls how large each parameter update is during training."),
    ],
    "Neural Networks": [
        ("What is a neuron in a neural network?", "A weighted computation plus activation", "A database row", "A URL route", "A package manager", "option1", "Artificial neurons combine inputs with weights and pass the result through an activation."),
        ("What is a hidden layer?", "A layer between input and output", "A hidden file only", "A SQL index", "A browser cache", "option1", "Hidden layers learn intermediate representations."),
        ("What are model weights?", "Learned parameters", "Dataset filenames", "HTML tags", "Log messages", "option1", "Weights are adjusted during training to reduce loss."),
        ("Why normalize inputs for neural networks?", "Improve optimization stability", "Remove the target", "Disable gradients", "Increase leakage", "option1", "Scaled inputs often make gradient-based training faster and more stable."),
        ("What is gradient descent?", "An iterative optimization method", "A database query", "A plot type only", "A security protocol", "option1", "Gradient descent updates parameters in a direction that reduces loss."),
    ],
    "CNN": [
        ("What is a convolutional layer good at?", "Detecting local spatial patterns", "Managing user sessions", "Parsing SQL only", "Hashing passwords", "option1", "Convolutions learn local filters that are useful for images and grid-like data."),
        ("What does pooling often do?", "Reduces spatial resolution", "Creates passwords", "Adds labels", "Increases every dimension", "option1", "Pooling summarizes nearby activations and can reduce computation."),
        ("What is a kernel/filter in CNNs?", "A small learned weight grid", "A Flask template", "A database row", "A random seed only", "option1", "CNN filters slide over inputs to detect patterns such as edges or textures."),
        ("Why are CNNs parameter efficient for images?", "They share filter weights across locations", "They store every pixel as a table", "They avoid training", "They require no data", "option1", "Weight sharing lets the same detector operate across spatial positions."),
        ("What is padding used for?", "Control output size at borders", "Encrypt images", "Change labels", "Serve APIs", "option1", "Padding adds border values so convolutions can preserve or control spatial dimensions."),
    ],
    "RNN": [
        ("What are RNNs designed to process?", "Sequential data", "Only independent rows", "Static CSS", "SQL schemas", "option1", "RNNs pass hidden state through time, making them suitable for sequences."),
        ("What problem do LSTMs address?", "Long-range dependency learning", "Password hashing", "One-hot encoding only", "Table joins", "option1", "LSTMs use gates to reduce vanishing-gradient issues in sequence modeling."),
        ("What is hidden state?", "A memory vector carried across time steps", "A database password", "A chart title", "A file extension", "option1", "Hidden state summarizes earlier sequence information for later predictions."),
        ("What is teacher forcing?", "Feeding true previous tokens during training", "Letting users answer twice", "Deploying without tests", "Deleting labels", "option1", "Teacher forcing can stabilize sequence decoder training."),
        ("Why can vanilla RNNs struggle with long sequences?", "Vanishing or exploding gradients", "Too many CSS files", "No database table", "No random numbers", "option1", "Repeated multiplication through time can shrink or amplify gradients."),
    ],
    "Transformers": [
        ("What is self-attention?", "Relating tokens to other tokens in the same sequence", "A login method", "A SQL join only", "A CNN filter", "option1", "Self-attention lets each token weigh information from other positions."),
        ("Why do transformers use positional information?", "Attention alone has no inherent token order", "To hash passwords", "To resize images only", "To store sessions", "option1", "Position encodings or embeddings tell the model where tokens occur."),
        ("What is multi-head attention?", "Several attention projections in parallel", "Several databases", "Several passwords", "Several CSS files", "option1", "Multiple heads let the model attend to different relationship patterns."),
        ("What is a transformer encoder commonly used for?", "Understanding and representing input sequences", "Only generating images", "Only database migration", "Only serving static files", "option1", "Encoder stacks produce contextual representations for tasks like classification or retrieval."),
        ("What is causal masking?", "Preventing attention to future tokens", "Masking usernames", "Removing all data", "Disabling gradients", "option1", "Causal masks preserve autoregressive generation by hiding future positions."),
    ],
    "TensorFlow": [
        ("What is Keras in TensorFlow?", "A high-level neural network API", "A database engine", "A browser plugin", "A CSS utility", "option1", "Keras provides convenient layers, models, training loops, and callbacks."),
        ("What does tf.data help build?", "Efficient input pipelines", "HTML pages", "Password hashes", "SQL joins", "option1", "tf.data supports batching, shuffling, mapping, and prefetching data."),
        ("What is a TensorFlow tensor?", "A multidimensional numeric data object", "A Flask route", "A markdown file", "A SQL index", "option1", "Tensors are the core data representation in TensorFlow computations."),
        ("What does model.fit() do in Keras?", "Runs training over data", "Starts a web server", "Creates a database", "Encrypts features", "option1", "model.fit trains a compiled Keras model for one or more epochs."),
        ("What are TensorFlow callbacks used for?", "Hooking actions into training events", "Changing CSS colors", "Creating passwords", "Deleting labels", "option1", "Callbacks can perform early stopping, checkpoints, logging, and learning-rate scheduling."),
    ],
    "PyTorch": [
        ("What is autograd in PyTorch?", "Automatic gradient computation", "Automatic web routing", "Automatic SQL indexing", "Automatic CSS layout", "option1", "Autograd tracks tensor operations and computes gradients for optimization."),
        ("What is nn.Module?", "Base class for neural network components", "A database migration", "A browser module", "A CSV parser only", "option1", "PyTorch models and layers are usually organized as nn.Module subclasses."),
        ("What does optimizer.step() do?", "Updates parameters using gradients", "Loads a template", "Splits a DataFrame", "Hashes a password", "option1", "After gradients are computed, optimizer.step applies parameter updates."),
        ("Why call model.eval()?", "Switch layers to inference behavior", "Delete gradients forever", "Start Flask", "Create a table", "option1", "Evaluation mode changes behavior for layers such as dropout and batch normalization."),
        ("What is a DataLoader used for?", "Batching and iterating over datasets", "Serving HTML", "Creating badges", "Writing SQL only", "option1", "DataLoader handles batching, shuffling, and parallel data loading."),
    ],
    "Scikit-learn": [
        ("What is fit() in scikit-learn?", "Learn parameters from training data", "Render HTML", "Open a socket", "Hash a password", "option1", "fit estimates model or transformer parameters from data."),
        ("What is transform() used for?", "Apply a learned preprocessing step", "Train a Flask route", "Update a password", "Deploy a model only", "option1", "Transformers use transform to apply learned scaling, encoding, or projection."),
        ("Why use a Pipeline?", "Chain preprocessing and modeling safely", "Style a page", "Create sessions", "Generate passwords", "option1", "Pipelines reduce leakage and make workflows reproducible."),
        ("What does train_test_split do?", "Splits arrays into train and test subsets", "Normalizes labels only", "Compiles tensors", "Creates routes", "option1", "train_test_split quickly creates held-out data for evaluation."),
        ("What is GridSearchCV?", "Hyperparameter search with cross-validation", "A CSS grid helper", "A database table", "A password checker", "option1", "GridSearchCV evaluates parameter combinations across validation folds."),
    ],
    "MLOps": [
        ("What is model monitoring?", "Tracking production model behavior", "Only plotting training loss", "Only writing CSS", "Only deleting logs", "option1", "Monitoring watches metrics, drift, latency, and failures after deployment."),
        ("What is data drift?", "Production data distribution changes", "A syntax error", "A missing route", "A password reset", "option1", "Data drift can reduce model performance when real-world inputs shift."),
        ("Why version datasets and models?", "Reproducibility and rollback", "More CSS animations", "Automatic accuracy", "No need for tests", "option1", "Versioning helps teams reproduce experiments and recover from bad releases."),
        ("What is CI/CD for ML?", "Automating tests, packaging, and deployment", "A clustering algorithm", "A loss function", "A token type", "option1", "ML CI/CD validates code, data, and model artifacts before release."),
        ("What is a model registry?", "A catalog of model versions and metadata", "A browser cache", "A password vault only", "A CSS file", "option1", "Registries track model artifacts, stage, metrics, and lineage."),
    ],
    "Generative AI": [
        ("What does generative AI produce?", "New content from learned patterns", "Only database backups", "Only validation splits", "Only password hashes", "option1", "Generative models can create text, images, audio, code, or other data-like outputs."),
        ("What is a diffusion model often used for?", "Image generation", "SQL indexing", "Password hashing", "Data joins", "option1", "Diffusion models learn to reverse a noise process to generate samples."),
        ("What is sampling temperature?", "A control for randomness in generation", "GPU heat only", "Batch size only", "Database timeout", "option1", "Higher temperature usually makes generated text more diverse and less deterministic."),
        ("What is a latent space?", "Compressed learned representation space", "A hidden webpage", "A database schema", "A CSS layer", "option1", "Generative models often manipulate compact latent representations to produce outputs."),
        ("What is hallucination in generative AI?", "Plausible but false generated content", "A perfect citation", "A database lock", "A training epoch", "option1", "Models can generate confident statements that are not grounded in facts."),
    ],
    "Prompt Engineering": [
        ("What is a system prompt?", "Instruction setting model behavior and constraints", "A shell password", "A SQL trigger", "A dataset split", "option1", "System prompts guide the model's role, priorities, and boundaries."),
        ("Why provide examples in a prompt?", "Demonstrate the desired pattern", "Increase database size", "Disable reasoning", "Change screen width", "option1", "Few-shot examples can steer format, style, and task behavior."),
        ("What is prompt injection?", "Malicious or conflicting instructions inserted into context", "A neural optimizer", "A CSS class", "A Pandas method", "option1", "Prompt injection tries to override intended instructions or extract protected information."),
        ("Why specify output format?", "Make responses easier to parse and use", "Guarantee zero errors", "Train a model from scratch", "Encrypt text", "option1", "Clear formats reduce ambiguity and simplify downstream processing."),
        ("What is chain-of-thought prompting meant to encourage?", "Stepwise reasoning behavior", "Image compression", "Password rotation", "SQL joins", "option1", "Reasoning prompts can encourage models to break complex tasks into intermediate steps."),
    ],
    "LLMs": [
        ("What does LLM stand for?", "Large Language Model", "Linear Loss Machine", "Local Label Matrix", "Layered Logic Map", "option1", "LLM means Large Language Model, a model trained on large-scale text or multimodal corpora."),
        ("What is tokenization?", "Splitting text into model-readable units", "Encrypting sessions", "Fitting a scaler", "Drawing charts", "option1", "Tokenizers convert text into token IDs consumed by language models."),
        ("What is context window?", "The amount of input and output tokens a model can consider", "Browser width", "Database row count", "Learning rate", "option1", "The context window limits how much conversation or document text can be processed at once."),
        ("What is fine-tuning?", "Further training a model on task-specific data", "Only changing a prompt", "Only resizing a tensor", "Creating a Flask route", "option1", "Fine-tuning updates model parameters using additional data for a target behavior."),
        ("What is retrieval-augmented generation?", "Grounding generation with retrieved external information", "Only random sampling", "Only model compression", "Only UI rendering", "option1", "RAG retrieves relevant sources and includes them as context for generation."),
    ],
}

DIFFICULTIES = ["easy", "medium", "hard"]


def make_questions():
    questions = []
    distractor_sets = [
        ("It improves test accuracy without validation.", "It removes the need for data cleaning.", "It is mainly a UI styling technique."),
        ("It only applies to image files.", "It guarantees causation.", "It disables model training."),
        ("It is a database-only operation.", "It requires no assumptions.", "It always increases overfitting."),
    ]

    prompt_variants = [
        "In a production ML workflow, which answer best fits this concept?",
        "During interview prep, how should this idea be understood?",
        "When debugging an ML pipeline, which interpretation is most accurate?",
        "For a practical data science project, what is the best description?",
        "In model development notes, which statement should be marked correct?",
        "When reviewing fundamentals, which option captures the main point?",
        "For an applied ML system, which explanation is most reliable?",
        "In an experiment report, which description would be technically accurate?",
        "When teaching this topic to a teammate, which answer is clearest?",
        "For exam-style ML reasoning, which option is correct?",
    ]

    for category, seeds in CATEGORIES.items():
        for i in range(300):
            base = seeds[i % len(seeds)]
            suffix = (
                ""
                if i < len(seeds)
                else f" {prompt_variants[(i - len(seeds)) % len(prompt_variants)]} Case #{i - len(seeds) + 1}."
            )
            wrongs = distractor_sets[i % len(distractor_sets)]
            questions.append(
                {
                    "category": category,
                    "question": base[0] + suffix,
                    "option1": base[1],
                    "option2": base[2] if i < len(seeds) else wrongs[0],
                    "option3": base[3] if i < len(seeds) else wrongs[1],
                    "option4": base[4] if i < len(seeds) else wrongs[2],
                    "correct_answer": base[5],
                    "explanation": base[6],
                    "difficulty": DIFFICULTIES[i % len(DIFFICULTIES)],
                }
            )
    return questions


if __name__ == "__main__":
    output = Path(__file__).with_name("ml_questions.json")
    questions = make_questions()
    output.write_text(json.dumps(questions, indent=2), encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {output}")


