import sqlite3

DB_PATH = "./vectordb/kb.sqlite3"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kb_articles (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    resolution TEXT,
    incident_link TEXT
)
""")

articles = [
    ("kb001", "Internet connectivity fail", "Users cannot connect to Internet", "Restart gateway router", "https://servicenow/.../INC001"),
    ("kb002", "VPN login issue", "VPN timeout on login", "Reset VPN service", "https://servicenow/.../INC002"),
    ("kb003", "Not able to connect to Internet from Spokes network", "Users from the virtual machines dpeloyed in the spokes network not able to access Internet", "The spokes network custom route table do not forward the traffic for 0.0.0.0/0 to the firewall. This leads to assymetric routing. To fix this, we had to add a custom route in the route table to forward traffic to the firewall for 0.0.0.0/0. With this the incoming and return traffic passes through the firewalls", "https://servicenow/.../INC003"),
    ("kb004", "The URL google.com is not reachable", "Users not able to access google.com/ from the spokes virtual machine", "Goole.com is blocked in the firewalls. Users are requested to browse google.co.uk/ instead", "https://servicenow/.../INC004"),
    ("kb005", "Users from London datacenter not able to access the application UI hosted in cloud vnet", "Users from London datacenter not able to access the application UI hosted in cloud vnet", "The inbound NSG rule was blocking the traffic. To fix this we had to allow the connection in the inbound NSG rule", "https://servicenow/.../INC005"),
    ("kb006", "Algo application throwing insecure certificate issue", "While accessing the Algo application, browser throwing insecure certificate", "The vendor of the Algo application is SS&C who has informed to upgrade the application to next version 5.3. We have upgraded the application version which fixed the issue", "https://servicenow/.../INC006"),
    ("kb007", "Algo integration with Airflow not working", "Algo not able to work with Airflow application", "Algo application was not registered with Airflow. To fix this, we had to register the application with Airflow", "https://servicenow/.../INC007"),
    ("kb008", "EAP application throwing 404 error", "EAP application throwing 404 error", "The deployment of the application went into error last night. This was not discovered while testing. We had to redeploy the application to fix the issue", "https://servicenow/.../INC008"),
    ("kb009", "Mobility application throwing 404 error", "Mobility application throwing 404 error", "The deployment of the application went into error last night. This was not discovered while testing. We had to redeploy the application to fix the issue", "https://servicenow/.../INC009"),
    ("kb010", "ALPS application throwing 404 error", "ALPS application throwing 404 error", "The deployment of the application went into error last night. This was not discovered while testing. We had to redeploy the application to fix the issue", "https://servicenow/.../INC010"),
]

cursor.executemany("""
INSERT OR REPLACE INTO kb_articles (id, title, description, resolution, incident_link)
VALUES (?, ?, ?, ?, ?)
""", articles)

conn.commit()
conn.close()

print("SQLite KB database seeded!")