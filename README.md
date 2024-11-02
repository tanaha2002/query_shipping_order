### Problem Definition
- Base on the problem user can ask anything about related to their order, we need to determine the cluster of field that user may ask.

- After a bit of time thinking, i will define the user question to 4 cluster.
    - `Order Status`: Any question of user related to status of their order.
    - `Delivery Time`: Any question of user related to `time shipping`, `estimate time`,...
    - `Shipping Issue`: Any question of user related to problem of their order, like `wrong address`, `the order didn't come`, ...
    - `Out of Domain`: And the last one is that question of user not related to our problem.

- For `Order Status` it will have 7 status:
    - Order Recieved
    - Prepare for Shipment
    - Shipped
    - Out for Delivery
    - Delivered
    - Failed (contain reason)
    - Canceled (contain reason)
### Hand On
#### Prepare Data
- To create a classification model, I started by handcrafting questions. Each class has 40 questions, and `Out of Domain` class has 48 questions that I create for classification.

- However, with only about 168 questions, the data is too small to test methods. Then, before testing, I augmented my data.

- The augmentation methods I used include:
    - Synonym: Replace synonyms with other words from the `wordnet` set.
    - Random Swap: Random swap word in sentence.
    - Contextual Word Embeddings Augmenter: Using `Bert` and `Roberta` to add context to sentence.
- After augmentation, my data increased to about 670 sample (these 670 sample are the training set, it already split before augmentation to ensure the test set has more realistic sentences and it not augmented).

#### Craft a Model
- I tried basic machine learning models like `N-gram` and `logistic regression` with `TF-IDF`. The accuracy was about ~0.8 on the test set, but when I tested them myself, they were not very accurate. It seems my test set was too small and did not cover enough.

- Then I try to adjusted the test set a bit and train the models again, and also added new models like `Fasttext` and `DistilBert`. I used `DistilBert` instead of `Bert` because Distil is a lighter model, reducing up to 40% of parameters compared to `Bert`.

- After some testing, `DistilBert` give the best results. It achieved about ~0.96 on the test set and also performed well on the experimental test.

### Simple interactive App
- I created a sample database with 50 samples using SQLite3 to simulate user queries.

- The database is a simple `orders` table as follows:
    ```
    CREATE TABLE orders (
        orderid INTEGER,
        customerid INTEGER,
        customer_name TEXT,
        product_name TEXT,
        shipping_date_estimate DATE,
        order_status TEXT,
        reason TEXT
    );
    ```
- And finally, I created a simple CLI to interact with the database base on user question.
### Usage
- First, clone this repo and please download the model and tokenizer from this link: Link[https://drive.google.com/file/d/1mlPL5g5YhHKUmrW-YaoPY8VYTlI3uFDe/view?usp=sharing]
- Then put the model and tokenizer inside folder `models`, your repo will look like this:
    ```
    └───src
    ├───data
    ├───models
    │   ├───checkpoint-252
    │   └───distillbert-tokenizer
    ├───notebook
    ├───router
    └───utils
    ```
- Then install requirement from `requirements.txt` and go to `src` folder and run the `main.py` file via CLI.

### Demo


