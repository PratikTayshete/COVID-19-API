# COVID-19-API
A REST API to provide some information related to COVID-19 from a website using beautifulsoup4 and Flask.

The information provided by the REST API is scraped from the given website: https://www.mohfw.gov.in/

The REST API provides the following information:

  - Overall statistics about cases.
  
  - Contact information for COVID-19 queries.
  
  - Total vaccination count.
  
 
Prerequisites:

 - Install Docker and Docker-Compose

    - https://docs.docker.com/install/linux/docker-ce/ubuntu/

    - https://docs.docker.com/docker-for-windows/install/

    - https://docs.docker.com/compose/install/

Run the Flask app via docker (from the parent directory):

    docker-compose build 
    docker-compose up

References:

 - https://docs.docker.com/
 - https://hub.docker.com/