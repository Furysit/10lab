import random

# Параметры генетического алгоритма
POPULATION_SIZE = 100  # Размер популяции
MUTATION_RATE = 0.1    # Вероятность мутации
MAX_GENERATIONS = 1000  # Максимальное количество поколений

# Целевой пароль
TARGET_PASSWORD = "hello123"
# Символы, допустимые в пароле
CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Функция создания случайной строки
def generate_random_string(length):
    return ''.join(random.choice(CHARACTERS) for _ in range(length))

# Инициализация начальной популяции
def initialize_population(size, length):
    return [generate_random_string(length) for _ in range(size)]

# Функция оценки пригодности (fitness): количество совпадающих символов
def fitness_function(candidate):
    return sum(1 for c, t in zip(candidate, TARGET_PASSWORD) if c == t)

# Отбор лучших кандидатов (селекция)
def select_parents(population, fitness_scores):
    # Пропорциональный отбор (рулетка)
    total_fitness = sum(fitness_scores)
    selection_probs = [score / total_fitness for score in fitness_scores]
    return random.choices(population, weights=selection_probs, k=2)

# Операция скрещивания (crossover)
def crossover(parent1, parent2):
    split_point = random.randint(0, len(parent1) - 1)
    child = parent1[:split_point] + parent2[split_point:]
    return child

# Операция мутации
def mutate(candidate):
    candidate = list(candidate)
    for i in range(len(candidate)):
        if random.random() < MUTATION_RATE:
            candidate[i] = random.choice(CHARACTERS)
    return ''.join(candidate)

# Основная функция генетического алгоритма
def genetic_algorithm():
    generation = 0
    population = initialize_population(POPULATION_SIZE, len(TARGET_PASSWORD))

    while generation < MAX_GENERATIONS:
        # Вычисляем пригодность каждого кандидата
        fitness_scores = [fitness_function(candidate) for candidate in population]

        # Проверяем, найден ли целевой пароль
        if TARGET_PASSWORD in population:
            print(f"Пароль найден: {TARGET_PASSWORD} в поколении {generation}")
            return

        # Создаём новое поколение
        new_population = []
        for _ in range(POPULATION_SIZE):
            parent1, parent2 = select_parents(population, fitness_scores)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
        generation += 1

        # Выводим промежуточный результат
        best_fitness = max(fitness_scores)
        best_candidate = population[fitness_scores.index(best_fitness)]
        print(f"Поколение {generation}: Лучший результат = {best_candidate} (пригодность {best_fitness})")

    print("Целевой пароль не найден. Попробуйте увеличить количество поколений.")

# Запуск программы
if __name__ == "__main__":
    genetic_algorithm()
