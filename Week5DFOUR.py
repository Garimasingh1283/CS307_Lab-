import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import yfinance as yf
from hmmlearn import hmm
import numpy as np
import matplotlib.pyplot as plt


# --- Bayesian Network and Naive Bayes ---
def bayesian_network_and_naive_bayes():
    # Load the dataset
    data = pd.read_csv("2020_bn_nb_data.txt", sep="\t")

    # Define the structure of the Bayesian Network
    model = BayesianNetwork([('EC100', 'PH100'), ('IT101', 'PH100'), ('MA101', 'PH100')])

    # Fit the model using Maximum Likelihood Estimation
    model.fit(data, estimator=MaximumLikelihoodEstimator)
    inference = VariableElimination(model)

    # Predict grade in PH100 based on EC100, IT101, MA101
    query_result = inference.query(variables=['PH100'], evidence={'EC100': 'DD', 'IT101': 'CC', 'MA101': 'CD'})
    print("Bayesian Network Prediction (PH100):")
    print(query_result)

    # Prepare the data for Naive Bayes Classifier
    X = data.drop(columns=['Internship'])
    y = data['Internship']

    # Naive Bayes Classifier (Independent Features)
    accuracies = []
    for i in range(20):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=i)

        # Train Naive Bayes (independent features)
        nb_model = GaussianNB()
        nb_model.fit(X_train, y_train)
        y_pred = nb_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        accuracies.append(accuracy)
        print(f"Iteration {i+1} - Naive Bayes (Independent): Accuracy = {accuracy:.4f}")

    print(f"Average Accuracy (Naive Bayes - Independent): {np.mean(accuracies):.4f}")

    # Naive Bayes Classifier with Dependency (using Bayesian Network dependencies)
    dependent_accuracies = []
    for i in range(20):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=i)

        # Predict Internship based on Bayesian Network dependencies
        y_pred_dep = []
        for idx, row in X_test.iterrows():
            query_result = inference.map_query(variables=['Internship'], evidence=row.to_dict())
            y_pred_dep.append(query_result['Internship'])

        accuracy_dep = accuracy_score(y_test, y_pred_dep)
        dependent_accuracies.append(accuracy_dep)
        print(f"Iteration {i+1} - Naive Bayes (Dependent): Accuracy = {accuracy_dep:.4f}")

    print(f"Average Accuracy (Naive Bayes - Dependent): {np.mean(dependent_accuracies):.4f}")


# --- Gaussian Hidden Markov Model for Financial Time Series ---
def gaussian_hidden_markov_model():
    # Download historical stock data from Yahoo Finance
    data = yf.download('AAPL', start='2010-01-01', end='2020-12-31')

    # Calculate daily returns
    data['Return'] = data['Adj Close'].pct_change().dropna()
    data = data.dropna()

    # Prepare returns for the HMM model
    returns = data[['Return']].values

    # Fit a Gaussian Hidden Markov Model with 2 hidden states
    model = hmm.GaussianHMM(n_components=2, covariance_type="full", n_iter=1000)
    model.fit(returns)

    # Predict hidden states for the returns
    hidden_states = model.predict(returns)

    # Plot returns and hidden states
    plt.figure(figsize=(15, 8))
    plt.plot(data.index, data['Return'], label='Returns')
    plt.scatter(data.index, hidden_states, c=hidden_states, cmap='coolwarm', label="Hidden States", alpha=0.5)
    plt.legend()
    plt.title('Stock Returns and Hidden States')
    plt.show()

    # Print transition matrix and means of hidden states
    print("Transition Matrix:\n", model.transmat_)
    print("Means of hidden states:", model.means_)
    print("Variances of hidden states:", [np.diag(cov) for cov in model.covars_])

    # Plot hidden states over time
    data['Hidden State'] = hidden_states
    plt.figure(figsize=(15, 8))
    for i in range(model.n_components):
        state = (hidden_states == i)
        plt.plot(data.index[state], returns[state], '.', label=f"Hidden State {i}")
    plt.legend()
    plt.title('Hidden States Over Time')
    plt.show()


if _name_ == "_main_":
    # Run Bayesian Network and Naive Bayes experiments
    bayesian_network_and_naive_bayes()

    # Run Gaussian Hidden Markov Model for financial time series
    gaussian_hidden_markov_model()