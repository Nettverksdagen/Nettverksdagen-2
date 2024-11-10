#!/bin/bash

# Define the text to search for as a variable
TEXT_TO_SEARCH="Nettverksdagene"

# Loop to repeat the process 5 times
for i in {1..50}; do
    echo "Run #$i: Starting dependency update and installation..."

    # Step 1: Run dependency update and install
    npx dependency-time-machine --update --install || { echo "Error during dependency update and install. Aborting."; exit 1; }

    # Step 2: Start Docker containers in the background
    echo "Starting Docker containers..."
    docker compose up -d || { echo "Error starting Docker containers. Aborting."; docker compose down; exit 1; }

    # Step 3: Wait for localhost:8080 to become available with a retry limit
    echo "Waiting for localhost:8080 to become available..."
    retry_count=0
    max_retries=10
    until curl -s --head --request GET http://localhost:8080 | grep "200 OK" > /dev/null; do
        if [ $retry_count -ge $max_retries ]; then
            echo "Error: localhost:8080 is not reachable after $max_retries attempts. Aborting script."
            docker compose down
            exit 1
        fi
        echo "Waiting for localhost:8080 to be reachable... Attempt #$((retry_count + 1))"
        sleep 5
        ((retry_count++))
    done

    echo "localhost:8080 is now reachable!"

    # Step 4: Check for specific text on the homepage with a retry limit
    echo "Checking for text '$TEXT_TO_SEARCH' on the homepage..."
    text_retry_count=0
    max_text_retries=10
    until curl -s http://localhost:8080 | grep -q "$TEXT_TO_SEARCH"; do
        if [ $text_retry_count -ge $max_text_retries ]; then
            echo "Error: Text '$TEXT_TO_SEARCH' not found on the homepage after $max_text_retries attempts. Aborting script."
            docker compose down
            exit 1
        fi
        echo "Text '$TEXT_TO_SEARCH' not found on the homepage. Retrying... Attempt #$((text_retry_count + 1))"
        sleep 5
        ((text_retry_count++))
    done

    echo "Text '$TEXT_TO_SEARCH' found on the homepage!"
    
    # Step 5: Stop and remove the containers before the next loop
    echo "Stopping Docker containers..."
    docker compose down frontend || { echo "Error stopping Docker containers. Aborting."; exit 1; }

    # Optional: wait between runs if desired
    echo "Waiting before the next run..."
    sleep 1
done

echo "Script completed successfully after 5 runs."
