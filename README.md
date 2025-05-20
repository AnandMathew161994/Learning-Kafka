# Basics 
    Port : 
      1 : 2 
      3 : 4 
      -- This talks about ports on the container side 
      KAFKA_CFG_LISTENERS: PLAINTEXT://:2,CONTROLLER://:9093, EXTERNAL://:4
      
      -- This talks about the ports were kafka can be reached externally 
        -- If it has to be reaached from the host machine, it should say localhost , if another container on the same network needs to talk, then use the service name "kafka" 
      KAFKA_CFG_ADVERTISED_LISTENERS: PLAINTEXT://kafka:1,EXTERNAL://localhost:3
      
      KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,EXTERNAL:PLAINTEXT

 ####  Note - Although Host.docker.internal resolves to the localhost within the container , you cannot use producer = localhost  and advertised listener = host.docker.internal as once it resolves and connects , the host.docker.internal stays undefined for host machine
  ##### Its a one way bridge -- it allows container to talk to host, but can have host talk to container 
             Host.docker.internal is used within the container to access services running on host 
               -- container needs to talk to service on your host 
                   Postgres server on your host at localhost:5432
              -- Running kafka on host and client inside container --> Your containerized consumer needs to reach the host machines kafka port 
                  Its a one way bridge -- it allows container to talk to host, but can have host talk to container 
