
---

# Projeto Nuvem

## 📚 **Descrição do Projeto**

O **Projeto Nuvem** é uma aplicação desenvolvida com **FastAPI**, que interage com um banco de dados **PostgreSQL**. A aplicação foi containerizada usando **Docker** e as imagens resultantes foram publicadas no **Docker Hub**. Posteriormente, a aplicação foi implantada no **Kubernetes** utilizando o serviço **Amazon EKS** (Elastic Kubernetes Service). O objetivo principal é demonstrar a capacidade de desenvolver, containerizar e orquestrar uma aplicação web moderna utilizando ferramentas amplamente adotadas na indústria.

### **O que foi feito:**

- **Desenvolvimento da API:** Criação de uma API RESTful utilizando FastAPI para gerenciar operações CRUD.
- **Configuração do Banco de Dados:** Configuração de um banco de dados PostgreSQL para armazenamento de dados persistentes.
- **Containerização com Docker:** Criação de Dockerfiles para a API e o PostgreSQL, permitindo a execução consistente em diferentes ambientes.
- **Publicação no Docker Hub:** Upload das imagens Docker para o Docker Hub, facilitando a distribuição e implantação.
- **Orquestração com Docker Compose:** Configuração de um arquivo `compose.yml` para orquestrar os serviços da API e do banco de dados.
- **Implantação no Kubernetes com Amazon EKS:** Utilização do Amazon EKS para gerenciar os contêineres, garantindo escalabilidade e resiliência.

## 🚀 **Como Executar a Aplicação**

### **Pré-requisitos**

- [Docker](https://www.docker.com/get-started) instalado na máquina.
- [Docker Compose](https://docs.docker.com/compose/install/) instalado.
- Conta no [Docker Hub](https://hub.docker.com/) para acessar as imagens.
- [kubectl](https://kubernetes.io/docs/tasks/tools/) instalado.
- [eksctl](https://eksctl.io/) instalado.
- Conta na [AWS](https://aws.amazon.com/) configurada com as devidas permissões para criar recursos no EKS.

### **Passo a Passo**

#### **1. Dockerizing da Aplicação**

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/sousa04/projeto-nuvem.git
   cd projeto-nuvem
   ```

2. **Executar o Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Verificar os Serviços:**
   - A API estará disponível em `http://localhost:8000`.
   - A documentação interativa estará em `http://localhost:8000/docs`.

4. **Parar os Serviços:**
   ```bash
   docker-compose down
   ```

#### **2. Implantação no Kubernetes com Amazon EKS**

1. **Criar o Cluster EKS:**
   ```bash
   eksctl create cluster --name projeto-nuvem-cluster-2 --region us-east-2 --nodegroup-name workers --node-type t2.micro --nodes 2 --nodes-min 1 --nodes-max 3
   ```
   - **Aguardar a Criação Completa:** 

2. **Aplicar os Arquivos de Configuração Kubernetes:**
   ```bash
   kubectl apply -f postgres-deployment.yml
   kubectl apply -f service.yml
   kubectl apply -f deployment.yml
   ```

3. **Verificar os Recursos Implantados:**
   ```bash
   kubectl get pods
   kubectl get services
   ```

4. **Acessar a Aplicação:**
   - Obtenha o `EXTERNAL-IP` do serviço `fastapi-service`:
     ```bash
     kubectl get services
     ```
   - Abra no navegador:
     ```
     http://<EXTERNAL-IP>/docs
     ```

## 📄 **Documentação dos Endpoints da API**

A API possui os seguintes endpoints:

| Método | Endpoint     | Descrição                              |
|--------|--------------|----------------------------------------|
| GET    | `/`          | Retorna uma mensagem de boas-vindas.   |
| POST   | `/registrar` | Registra um novo usuário.              |
| POST   | `/login`     | Autentica um usuário e retorna um token.|
| GET    | `/consultar` | Retorna dados protegidos (requere autenticação). |

### **Detalhes dos Endpoints**

1. **Registrar Usuário**
   - **URL:** `/registrar`
   - **Método:** `POST`
   - **Body:**
     ```json
     {
       "username": "seu_usuario",
       "password": "sua_senha"
     }
     ```
   - **Resposta:**
     ```json
     {
       "message": "Usuário registrado com sucesso."
     }
     ```

2. **Login**
   - **URL:** `/login`
   - **Método:** `POST`
   - **Body:**
     ```json
     {
       "username": "seu_usuario",
       "password": "sua_senha"
     }
     ```
   - **Resposta:**
     ```json
     {
       "access_token": "seu_token_jwt",
       "token_type": "bearer"
     }
     ```

3. **Consultar Dados Protegidos**
   - **URL:** `/consultar`
   - **Método:** `GET`
   - **Headers:**
     ```
     Authorization: Bearer seu_token_jwt
     ```
   - **Resposta:**
     ```json
     {
       "data": "Seus dados protegidos aqui."
     }
     ```

## 🖼️ **Screenshot com os Endpoints Testados**

![Endpoints Testados](imgs/testeDocker.jpeg)

*Exemplo de uso da documentação interativa com os endpoints sendo testados, ao rodar o arquivo testeDocker ou testeAWS.*

## 🐳 **Link para o Docker Hub do Projeto**

[Acesse a imagem Docker da API no Docker Hub](https://hub.docker.com/r/sousa04/projeto_nuvem)

## 📁 **Localização dos Arquivos de Configuração Kubernetes**

Os arquivos de configuração Kubernetes estão localizados na raiz do repositório:

- [`deployment.yml`](./deployment.yml)
- [`postgres-deployment.yml`](./postgres-deployment.yml)
- [`service.yml`](./service.yml)

### **Conteúdo dos Arquivos**

#### **1. `deployment.yml` (FastAPI)**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  labels:
    app: fastapi
    owner: sousa04
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi-app
          image: sousa04/projeto_nuvem:latest  
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              value: "postgresql://projeto:projeto@postgres:5432/projeto"
            - name: SECRET_KEY
              value: "mysecretkey" 
```

#### **2. `postgres-deployment.yml` (PostgreSQL)**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  labels:
    app: postgres
    owner: sousa04
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:17  # A imagem que você usa no Docker
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: "projeto"
            - name: POSTGRES_USER
              value: "projeto"
            - name: POSTGRES_PASSWORD
              value: "projeto"
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-storage
          emptyDir: {}
```

#### **3. `service.yml` (Serviços)**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  labels:
    app: fastapi
    owner: sousa04
spec:
  type: LoadBalancer  # Exposição externa via LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
      protocol: TCP
  selector:
    app: fastapi

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  labels:
    app: postgres
    owner: sousa04
spec:
  type: ClusterIP  # Tipo explícito
  ports:
    - port: 5432
      targetPort: 5432
      protocol: TCP
  selector:
    app: postgres
```

---

## ☁️ **Componentes do Projeto**

### **1. Amazon EKS (Elastic Kubernetes Service)**

O **Amazon EKS** gerencia automaticamente a infraestrutura do Kubernetes, garantindo alta disponibilidade e escalabilidade da aplicação. Os principais componentes configurados no EKS incluem:

- **Cluster EKS:** Ambiente gerenciado onde os nós (workers) do Kubernetes estão hospedados.
- **Node Groups:** Conjuntos de instâncias EC2 que executam os pods da aplicação.
- **IAM Roles:** Permissões gerenciadas para os componentes do Kubernetes interagirem com outros serviços da AWS.

### **2. Kubernetes Components**

- **Deployments:**
  - **fastapi-app:** Gerencia a implantação da aplicação FastAPI, garantindo que o número desejado de réplicas esteja sempre em execução.
  - **postgres:** Gerencia a implantação do banco de dados PostgreSQL, garantindo alta disponibilidade.

- **Services:**
  - **fastapi-service:** Serviço do tipo LoadBalancer que expõe a API FastAPI externamente.
  - **postgres:** Serviço do tipo ClusterIP que permite a comunicação interna entre a aplicação FastAPI e o banco de dados PostgreSQL.

### **3. Docker Hub**

As imagens Docker da aplicação FastAPI e do PostgreSQL foram publicadas no Docker Hub para facilitar a distribuição e implantação.

- **FastAPI:** [sousa04/projeto_nuvem](https://hub.docker.com/r/sousa04/projeto_nuvem)
- **PostgreSQL:** Utiliza a imagem oficial `postgres:17`

### **4. IAM Roles e Permissões**

Para a integração com o Amazon EKS, foram configurados **IAM Roles** específicos que permitem ao cluster Kubernetes interagir com outros serviços da AWS, garantindo segurança e controle de acesso adequado.

---

## 📂 **Repositório do Projeto**

[Repositório no GitHub](https://github.com/sousa04/projeto-nuvem)

### **Estrutura do Repositório**

```
projeto-nuvem/
├── 📂 app/
│   ├── auth_utils.py
│   ├── db.py
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│── 📂 imgs/
│   └── testeDocker.jpeg
├── 📂 videos/
│   ├── testeDockerinzing.mp4
│   └── video_entrega_aws.mp4
├── .env
├── .gitignore
├── compose.yml
├── deployment.yml
├── Infos.ttx
├── postgres-deployment.yml
├── README.md
├── service.yml
├── testeAWS.py
└── testeDocker.py

```

## 🔗 **Links Úteis**

- **Docker Hub:** [sousa04/projeto_nuvem](https://hub.docker.com/r/sousa04/projeto_nuvem)
- **Repositório do Projeto:** [GitHub - sousa04/projeto-nuvem](https://github.com/SousaThiago749/Projeto-Nuvem)
- **Documentação do Docker Compose:** [Docker Compose Documentation](https://docs.docker.com/compose/)
- **Documentação do Kubernetes:** [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- **Documentação do Amazon EKS:** [EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)

