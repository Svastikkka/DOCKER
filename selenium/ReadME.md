# Document the steps you followed, including any challenges faced and solutions implemented.
Below is a step-by-step guide on how to create and set up your project, including creating the requirements.txt, script.py, Dockerfile, and docker-compose.yml files:
- Create the requirements.txt file: In your project directory, create a requirements.txt file to list all the Python libraries required for your script. For example:
```
pymongo
selenium
```

- Write the script.py logic: In the script directory of your project, create the script.py file and add the logic for your web scraping script. Use the script you provided earlier as an example.
- Write the Dockerfile: In your project directory, create a Dockerfile to build the Docker image for your script. The Dockerfile should contain the necessary instructions to install the required Python libraries from the requirements.txt and copy the script.py into the image. Here's an example Dockerfile:

```
# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the necessary dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY script/script.py .

# Command to run the script
CMD ["python", "script.py"]
```

- Write the docker-compose.yml: In your project directory, create a docker-compose.yml file to define your Docker services and network. Use the build option for the scraper service to automatically build the Docker image from the Dockerfile.

- In docker-compose.yml, we use the build option for the scraper service to automatically build the Docker image for the script.py using the Dockerfile in the current directory.
With these steps, you have created your project, including the necessary files for web scraping using Selenium, and set up Docker to run the web scraping script in a scalable and distributed manner. Simply run docker-compose up in your project directory to start the scraping process.

#  Provide clear instructions on how to reproduce your setup and deployment process. 
- Step 1: Unzip The zip file
- Step 2: Run docker compose command to setup locally `docker-compose up -d --scale selenium-node-1=2`
- Step 3: Check logs inside ./logs/scraping.log
- Step 4: Selenium hub is exposed and running on `localhost:4444`

# Prepare a presentation summarizing your approach, highlighting the key decisions made, and showcasing the final solution.

The script you provided is a good fit for executing Selenium web scraping tasks efficiently for the following reasons:

1. Concurrency with ThreadPoolExecutor: The script utilizes the ThreadPoolExecutor from Python's concurrent.futures module to achieve concurrency. This allows the script to run multiple instances of the scrape_page function concurrently on different threads. Each instance can handle a range of pages, effectively distributing the scraping workload across multiple threads.
2. Asynchronous Execution: By using ThreadPoolExecutor, the script can execute multiple instances asynchronously. This means that while one instance is scraping a page, other instances can simultaneously handle other pages. Asynchronous execution helps improve the overall scraping performance and reduces the time taken to complete the entire scraping process.
3. Scalability: The script is designed to be easily scalable. You can specify the number of instances (Selenium nodes) using the num_instances variable. With this setup, you can easily scale the number of instances to process more pages concurrently, allowing you to handle larger scraping tasks efficiently.
4. Headless Browsing: The script uses headless browsing by enabling the --headless option for Chrome. Headless mode allows the browser to run without a graphical user interface, reducing resource usage and improving the scraping speed.
5. Clean Logging: The script implements clean logging using Python's logging module. Instead of printing messages to the console, it logs the scraping status and information to a file. This helps in debugging and monitoring the scraping process.
6. Dynamic Page URL Generation: The script dynamically generates the page URLs to be scraped based on the page variable, allowing it to navigate through multiple pages of the website seamlessly.
7. Robust Data Storage: The script stores the scraped data in MongoDB using the pymongo library. MongoDB is a scalable NoSQL database, which makes it a suitable choice for storing large amounts of data in a flexible JSON-like format.

Overall, the script follows good practices for concurrent web scraping, logging, and data storage, making it a well-suited solution for efficiently scraping web pages using Selenium. Its scalability and asynchronous execution make it capable of handling various scraping tasks, from small to large-scale projects.




