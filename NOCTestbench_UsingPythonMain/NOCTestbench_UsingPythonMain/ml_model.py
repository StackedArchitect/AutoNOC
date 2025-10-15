import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers
from modules.helper import NOCHelper


# Define the neural network architecture
def create_model(input_shape):
    model = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=input_shape),
        layers.Dense(32, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='sigmoid')  # Sigmoid activation for binary outputs
    ])
    return model
class NoCEnv:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.explored = np.zeros((rows, cols), dtype=bool)  # Initialize explored matrix
        self.state = None  # Initialize state (will be updated in reset())

    def reset(self):
        self.explored = np.zeros((self.rows, self.cols), dtype=bool)  # Reset exploration for each episode
        self.state = np.concatenate((self.explored.flatten(), np.zeros(2, dtype=bool)))  # Combine explored matrix and current pair
        return self.state

    def step(self, action):
        if action:  # Explore current pair
            self.explored[self.state[-2:]] = True  # Mark current pair as explored
            reward = not self.explored.all()  # Reward for finding unexplored pairs
        else:  # Move on to a new random pair
            new_source, new_dest = np.random.randint(0, self.rows, size=2)
            while self.explored[new_source, new_dest]:  # Ensure new pair is unexplored
                new_source, new_dest = np.random.randint(0, self.rows, size=2)
            self.state = np.concatenate((self.explored.flatten(), [bool(new_source), bool(new_dest)]))
            reward = 0  # No immediate reward for moving on, encourages exploration

        done = self.explored.all()  # Episode ends when full coverage is achieved

        return self.state, reward, done, {}  # Empty info dictionary (optional)

rows=2
columns=2
x=NOCHelper()
input_shape = (rows * 2 * columns,)  # Assuming concatenation of source and destination matrices
model = create_model(input_shape)
print(model.summary())


# Define hyperparameters (learning rate, discount factor, exploration parameters)
env = NoCEnv(rows, columns)  # Create the environment
agent = dqn_agent(env.observation_space.shape[0], env.action_space.n)  # Initialize the DQN agent

# Training loop
for episode in range(10):
    state = env.reset()
    done = False
    while not done:
        # Agent takes an action based on the current state
        action = agent.act(state)

        # Perform action in the environment, receive next state, reward, and done flag
        next_state, reward, done, _ = env.step(action)

        # Agent learns from the experience (state, action, reward, next_state)
        agent.learn(state, action, reward, next_state, done)

        state = next_state

    # Update agent parameters (e.g., replay buffer updates)
    agent.update()

# Save the trained agent for future use
agent.save_weights("trained_agent.h5")  # Replace with your saving mechanism
