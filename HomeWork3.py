# Импорт библиотек
import threading
from random import randint
from time import sleep


class Bank:
    def __init__(self):
        # Устанавливаем начальный баланс и блокировку
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        # Выполняем 100 операций пополнения
        for _ in range(100):
            with self.lock:  # Захватываем блокировку
                # Если баланс превышает 500 и замок заблокирован, разблокируем его
                if self.balance > 500 and self.lock.locked():
                    self.lock.release()
                # Генерируем случайное число для пополнения
                res = randint(50, 500)
                # Увеличиваем баланс
                self.balance += res
                # Выводим информацию о пополнении
                print(f'Пополнение: {res}. Баланс: {self.balance}')
            # Задержка для имитации выполнения
            sleep(0.001)

    def take(self):
        # Выполняем 100 операций снятия
        for _ in range(100):
            with self.lock:  # Блокировка для работы с балансом
                res = randint(50, 500)  # Генерация случайной суммы для снятия
                print(f'Запрос на {res}')
                if res <= self.balance:
                    self.balance -= res
                    print(f'Снятие: {res}. Баланс: {self.balance}')
                else:
                    print('Запрос отклонён, недостаточно средств')
                    self.lock.acquire()  # Блокируем поток, если средств не хватает


# Создаем объект банка
bk = Bank()

# Запускаем потоки для пополнения и снятия
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

# Запускаем потоки
th1.start()
th2.start()

# Ждем завершения работы потоков
th1.join()
th2.join()

# Выводим итоговый баланс
print(f'Итоговый баланс: {bk.balance}')
