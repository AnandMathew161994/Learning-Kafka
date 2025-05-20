## 🔌 Port Configuration

### 🔹 Port Mapping

```yaml
Port:
  1 : 2
  3 : 4
```

- **This mapping refers to ports on the container side.**

```bash
KAFKA_CFG_LISTENERS=PLAINTEXT://:2,CONTROLLER://:9093,EXTERNAL://:4
```

- **These are the ports where Kafka can be reached externally.**

  - If Kafka needs to be reached from the **host machine**, use:  
    `localhost`
  - If another **container on the same network** needs to connect, use:  
    `kafka` (i.e., the service name)
  - External listener connect to external advertised listener ( 3:4)
  - Internal ports (2) are used to connect to advertised listener on same network

```bash
KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:1,EXTERNAL://localhost:3
```

```bash
KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,EXTERNAL:PLAINTEXT
```

---

## ⚠️ Important Notes

### 🔸 About `host.docker.internal`

- If kafka on hostmachine (localhost) and producer in container pushing data at host.docker.internal ==> It work
- If kafka in docker listening at at host.docker.internal and producer on host machine  pushing data  ==> It wont work
- The reason it doesnt work is Kafka says "reach me at address"
  - When producer inside the container , host.docker.internal resolves to localhost and also kafka says "Reach me at localhost"
  - When producer in on host machine, kafka says "reach me at host.docker.internal" which is localhost of the contianer and not the port it should be listening and the host is unaware of host.docker.internal   

#### 🚧 One-Way Bridge 

- `host.docker.internal` creates a **one-way bridge**:
  - ✅ **Container ➡ Host** communication works. 
  - ❌ **Host ➡ Container** communication does **not** work by default.

---

### 💡 Usage Scenarios

- **Container needs to talk to a service on your host**  
  e.g., Postgres running on host at `localhost:5432`

- **Kafka running on host, and client running inside container**  
  e.g., A containerized consumer needs to reach the host machine's Kafka port.
