# Megamen, хакатон «Цифровой прорыв», кейс от Комитета информатизации и связи
Репозиторий для модели, споосбной адаптироваться к задачам определения корректного адреса, содержащегося в исходной базе данных.
UPD. docker: https://hub.docker.com/repository/docker/georgechufff/hacks_ai_spb/

**Содержание:**
1. Постановка проблемы
2. Описание решения
3. Развертка приложения
4. Демонстрация работы

# Проблематика кейсодержателя
В настоящее время при оформлении адресов (например, при заполнении заявки на ремонт) заполнители зачастую вводят данные по удобному для них формату, а не согласно одному из распространенных форматов — в связи с этим, понижается качество автоматической разметки (фактически невозможно создать rule-based решение, способное автоматически адаптироваться к любому введенному адресу), что ведет к дополнительным человеческим затратам (специалистам приходится самостоятельно просматривать и идентифицировать большое количество записей). 
Решения, используемые на данный момент, обладают несколькими недостатками:
1. Не используя в своей основе машинное обучение, решения не могут учесть все возможные случаи введенных данных;
2. Такие решения не обладают устойчивостью к неправильному вводу — например, в случаях опечатки/незнания верного наименования решение не сможет выдать верный ответ;
3. Ввиду не самого высокого качества таких решений, для корректной разметки приходится привлекать человеческие ресурсы, что влечет за собой дополнительные издержки. \

Внедрение нашего решения на основе систем машинного обучения позволит:
1. Повысить автоматизацию, качество и эффективность труда (работникам не придется заниматься ручной разметкой данных);
2. Увеличить качество и скорость обработки запросов; 
3. Уменьшит стоимость разметки данных (ввиду уменьшения ручной разметки специалистами).

# Описание решения
В поисках наиболее подходящего подхода были протестированы несколько возможных вариантов решения:
1. Ручная разметка данных по классам, решение задачи named entity recognition и последющий поиск наиболее релевантных запросов
2. Rule-based разметка данных
3. Получение эмбеддингов при помощи encoder-only моделей и последующее сравнение с эталонными адресами

Рассмотрим каждый из указанных подходов:
1. Ручная разметка достаточного количества объектов для обучения занимает продолжительное время, такое решение не сможет быстро адаптироваться к изменениям в данных, а сами ner-модели занимают много пространства и достаточно медленны в совершении предсказаний
2. Rule-based разметка (например, на основе регулярных выражений), неустойчива к опечаткам пользователей — даже в случае одной опечатки (попадания по соседней клавише, например) данный подход не сможет выдать верный результат
3. Новые модели (например, sentence-bert) обучены именно под поиск семантических схожестей, а также обладают высокой скоростью инференса даже на CPU. Из минусов можно отметить необходимость хранить векторные представления (эмбеддинги) под каждый объект базы данных

Исходя из требований к решению (масшатбируемость и высокое качество распознавания), было принято решение за основу взять третий подход — получение векторных представлений введенного пользователем объекта и поисх наиболее похожего в базе данных.

## Схема решения 
1. Получаем эмбеддинги бд
2. Конкатенируем
3. При помощи cosine_similarity определяем наиболее похожий объект

4. **ТУТ НУЖНА КАРТИНКА ТОГО КАК ОНО ВЫГЛЯДИТ И БЕНЧМАРКИ**

## Выбор моделей
** **

# Развертка приложения
``` docker build и сам контейнер```

# Демонстрация работы
** **
