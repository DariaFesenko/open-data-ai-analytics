# Infrastructure as Code in Azure (Terraform + Cloud-init)

## Overview

У цій роботі реалізовано повністю хмарне розгортання контейнеризованого застосунку в Microsoft Azure з використанням підходу Infrastructure as Code.

Інструменти:

* Terraform — створення інфраструктури
* Azure Cloud Shell — середовище виконання
* cloud-init — автоматична конфігурація VM
* Docker — запуск застосунку

---

##  Мета роботи

* навчитися працювати з Azure без локального середовища
* використовувати Terraform для створення ресурсів
* автоматизувати налаштування Linux VM через cloud-init
* розгорнути Docker-проєкт у хмарі

---

## Архітектура

```id="p9ak2f"
Azure
 ├── Resource Group
 ├── Virtual Network
 │    └── Subnet
 ├── Public IP
 ├── Network Security Group
 ├── Network Interface
 └── Linux Virtual Machine
        └── Docker (containers)
             ├── Web App
             ├── Database
             └── Data module
```

---

##  Розгортання

### 1. Відкрити Azure Cloud Shell

У браузері відкрити Azure Portal → Cloud Shell.

---

### 2. Перейти в каталог Terraform

```bash id="4kg8gh"
cd infra/terraform
```

---

### 3. Ініціалізація Terraform

```bash id="h2g7ws"
terraform init
```

---

### 4. Перевірка конфігурації

```bash id="sdj38f"
terraform fmt
terraform validate
```

---

### 5. Планування

```bash id="k93mdp"
terraform plan
```

---

### 6. Створення інфраструктури

```bash id="o91fks"
terraform apply
```

---

## Створені ресурси

Terraform створює:

* azurerm_resource_group
* azurerm_virtual_network
* azurerm_subnet
* azurerm_public_ip
* azurerm_network_security_group
* azurerm_network_interface
* azurerm_linux_virtual_machine

---

## cloud-init

Під час створення VM виконується cloud-init сценарій.

Основні дії:

```yaml id="r2d1ks"
package_update: true

packages:
  - git
  - docker.io
  - docker-compose

runcmd:
  - systemctl start docker
  - systemctl enable docker
  - git clone <repo_url> /app
  - cd /app
  - docker compose up -d
```

---

##  Розгортання застосунку

Після запуску VM автоматично:

* встановлюється Docker
* завантажується проєкт
* запускаються контейнери

---

##  Доступ до застосунку

Після `terraform apply` отримати Public IP:

```bash id="s8d1hs"
terraform output
```

Відкрити:

```id="k2j7hf"
http://PUBLIC_IP:5000
```

---

## Перевірка

Перевірка контейнерів:

```bash id="f91smd"
docker ps
```

Перевірка HTTP:

```bash id="z8c1aa"
curl http://PUBLIC_IP:5000
```

---

##  Видалення ресурсів

```bash id="m9d2as"
terraform destroy
```

---

## Можливі проблеми

* сайт не відкривається → перевірити NSG (порт 5000)
* Docker не запущений → перевірити cloud-init
* помилки контейнерів → перевірити `docker logs`

---

##  Висновки

У роботі було:

* створено інфраструктуру в Azure через Terraform
* автоматизовано налаштування VM через cloud-init
* розгорнуто Docker-застосунок без ручного втручання
* забезпечено доступ через public IP

---

##  Демонстрація

Необхідно показати:

* Terraform apply у Cloud Shell
* створену VM
* Public IP
* відкритий веб-застосунок

---


