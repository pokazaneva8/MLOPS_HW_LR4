# HW_3_Pokazaneva

This is my homework.

# ml_lab

## Установка

1. Установить зависимости через Poetry:
   ```bash
   poetry install
   ```
2. Запустить контейнер Docker с minio:
   ```bash
   docker compose up -d  # Или docker-compose up -d      
   ```
3. Установить права доступа:
   ```bash
   chmod +x ./pipeline.sh
   ```
4. Установка pre-commit:
   ```bash
   pre-commit install
   ```
   
5. Запустить pipeline.sh:
   ```bash
   export PYTHONPATH="$PYTHONPATH:$PWD" && ./pipeline.sh
   ```