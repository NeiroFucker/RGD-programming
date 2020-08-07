import time


class Station:
    def __init__(self, ways):
        self.ways = []
        for i in range(ways):
            while True:
                try:
                    capacity = int(input('Введите длину линии: '))
                    if capacity < 0:
                        print('Не понял, зачем отрицательные числа вводишь?')
                        continue
                    name = input('Введите название линии: ')
                    self.ways.append(Way(capacity, name))
                    break
                except ValueError:
                    print("Не понял, что началось то? Нормально общались!")

    def fill(self, train):
        s_ways = None
        for way in self.ways:
            if train.capacity <= way.capacity and way.filling is None \
               and (s_ways is None or s_ways.capacity > way.capacity):
                s_ways.append(way)

        if len(s_ways):
            _min = s_ways[0]
            for s_way in s_ways:
                if _min.capacity > s_way.capacity:
                    _min = s_way
            _min.filling = train
            return 'Поезд {train_name} занял линию {name}'.format(name=_min.name,
                                                                  train_name=_min.filling.name)
        return None

    def out_fill(self, train):
        for i in range(len(self.ways)):
            if self.ways[i].filling is None:
                continue
            elif self.ways[i].filling.name == train.name:
                out = 'Поезд {train_name} покинул линию {name}'.format(name=self.ways[i].name,
                                                                       train_name=self.ways[i].filling.name)
                self.ways[i].filling = None
                return out
        return None


class Way:
    def __init__(self, capacity, name, train=None):
        self.capacity = int(capacity)
        self.name = name
        self.filling = train


class Train:
    def __init__(self, name, capacity, arrive_time, out_time):
        self.capacity = int(capacity)
        self.name = name
        self.arrive_time = time.strptime(arrive_time, '%H%M')
        self.out_time = time.strptime(out_time, '%H%M')


trains = []
arrived_trains = []
while True:
    lines = input('Введите количество линий на станции: ')
    if lines.isdigit():
        break
station = Station(int(lines))

while True:
    n = input('Сколько поездов подъезжает: ')
    if not n.isdigit():
        print('Не понял, что за бред ты мне ввел?')
        continue
    break

for _ in range(int(n)):
    train_name = input('Введите id поезда: ')
    while True:
        train_capacity = input('Введите длину поезда: ')
        if train_capacity.isdigit():
            if int(train_capacity) >= 0:
                break
    while True:
        try:
            train_arriving = input('Введите время прибытия: ')
            if ':' in train_arriving:
                train_arriving = train_arriving.split(':')[0] + train_arriving.split(':')[1]
            time.strptime(train_arriving, '%H%M')
            break
        except ValueError:
            continue
    while True:
        try:
            train_outing = input('Введите время отбытия: ')
            if ':' in train_outing:
                train_outing = train_outing.split(':')[0] + train_outing.split(':')[1]
            time.strptime(train_outing, '%H%M')
            break
        except ValueError:
            continue
    trains.append(Train(train_name, train_capacity, train_arriving, train_outing))

trains = sorted(trains, key=lambda train: (train.out_time.tm_hour * 60 + train.out_time.tm_min) -
                                          (train.arrive_time.tm_hour * 60 + train.arrive_time.tm_min))

while True:
    for j in range(len(trains)):
        if (time.strptime(time.strftime('%H%M'), '%H%M') == trains[j].arrive_time) and \
                (trains[j] not in arrived_trains):
            result = station.fill(trains[j])
            if not result:
                print('Поезд {} не смог заехать'.format(trains[j].name))
                continue
            print(result)
            arrived_trains.append(trains[j])

    for train in arrived_trains:
        if train in trains:
            trains.remove(train)

    for arrived_train in arrived_trains:
        if time.strptime(time.strftime('%H%M'), '%H%M') == arrived_train.out_time:
            print(station.out_fill(arrived_train))
            arrived_trains.remove(arrived_train)
