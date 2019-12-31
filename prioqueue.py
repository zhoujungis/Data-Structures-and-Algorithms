from random import randint
from queue import SQueue
from error import PrioQueueError

class PrioQueue:
     def __init__(self, elist=[]):
         self._elems = list(elist)
         if elist:
             self.buildheap()
             
     def is_empty(self):
         return not self._elems
        
     def peek(self):
         if self.is_empty():
             raise PrioQueueError('in peek')
         return self._elems[0]
        
     def enqueue(self, e):
         self._elems.append(None)
         self.siftup(e, len(self._elems)-1)
         
     def siftup(self, e, last):
         elems, i, j = self._elems, last, (last-1)//2
         while i > 0 and e < elems[j]:
             elems[i] = elems[j]
             i, j = j, (j-1)//2
         elems[i] = e
         
     def dequeue(self):
         if self.is_empty():
             raise PrioQueueError('in dequeue')
         elems = self._elems
         e0 = elems[0]
         e = elems.pop()
         if len(elems) > 0:
             self.siftdown(e, 0, len(elems))
         return e0
        
     def siftdown(self, e, begin, end):
         elems, i, j = self._elems, begin, begin*2+1
         while j < end:
             if j+1 < end and elems[j+1] < elems[j]:
                 j += 1
             if e < elems[j]:
                 break
             elems[i] = elems[j]
             i, j = j, 2*j+1
         elems[i] = e
         
     def buildheap(self):
         end = len(self._elems)
         for i in range(end//2, -1, -1):
             self.siftdown(self._elems[i], i, end)

# 优先级队列应用实例——车站检查站模拟系统

class Simulation:
     def __init__(self, duration):
         self._eventq = PrioQueue()
         self._time = 0
         self._duration = duration
         
     def run(self):
         while not self._eventq.is_empty():
             event = self._eventq.dequeue()
             self._time = event.time()
             if self._time > self._duration:
                 break
             event.run()
             
     def add_event(self, event):
         self._eventq.enqueue(event)
         
     def cur_time(self):
         return self._time

class Event:
     def __init__(self, event_time, host):
         self._ctime = event_time
         self._host = host
         
     def __lt__(self, other):
         if not isinstance(other, Event):
             raise ValueError
         return self._ctime < other._ctime
        
     def __le__(self, other):
         if not isinstance(other, Event):
             raise ValueError
         return self._ctime <= other._ctime
        
     def host(self):
         return self._host
        
     def time(self):
         return self._ctime
        
     def run(self):
         pass

class Customs:
      def __init__(self, gate_num, duration, arrive_interval, check_interval):
          self.simulation = Simulation(duration)
          self.waitline = SQueue()
          self.duration = duration
          self.gates = [0] * gate_num
          self.total_wait_time = 0
          self.total_used_time = 0
          self.car_num = 0
          self.arrive_interval = arrive_interval
          self.check_interval = check_interval
          
      def wait_time_acc(self, n):
          self.total_wait_time += n
          
      def total_time_acc(self, n):
          self.total_used_time += n
          
      def car_count_1(self):
          self.car_num += 1
          
      def add_event(self, event):
          self.simulation.add_event(event)

      def cur_time(self):
          return self.simulation.cur_time()
        
      def enqueue(self, car):
          self.waitline.enqueue(car)
          
      def has_queued_car(self):
          return not self.waitline.is_empty()
        
      def next_car(self):
          return self.waitline.dequeue()
        
      def find_gate(self):
          for i in range(len(self.gates)):
              if self.gates[i] == 0:
                  self.gates[i] = 1
                  return i
          return None
        
      def free_gate(self, i):
          if self.gates[i] == 1:
              self.gates[i] == 0
          else:
              raise ValueError('Clear gate Error.')
            
      def simulate(self):
          Arrive(0, self)
          self.simulation.run()
          self.statistics()
          
      def statistics(self):
          print("Simulate " + str(self.duration) + " minutes, for " + str(len(self.gates)) + " gates")
          print(self.car_num, "cars pass the customs")
          print("Average waiting time:", self.total_wait_time / self.car_num)
          print("Average passing time:", self.total_used_time / self.car_num)
          i = 0
          while not self.waitline.is_empty():
              self.waitline.dequeue()
              i += 1
          print(i, "cars are in waiting line.")

class Car:
      def __init__(self, arrive_time):
          self.time = arrive_time
      def arrive_time(self):
          return self.time
 

def event_log(time, name):
      print("Event: " + name + ", happens at " + str(time))
      pass

class Arrive(Event):
      def __init__(self, arrive_time, customs):
          Event.__init__(self, arrive_time, customs)
          customs.add_event(self)
          
      def run(self):
          time, customs = self.time(), self.host()
          event_log(time, "car arrive")
          Arrive(time + randint(*customs.arrive_interval), customs)
          car = Car(time)
          if customs.has_queued_car():
              customs.enqueue(car)
              return
          i = customs.find_gate()
          if i is not None:
              event_log(time, "car check")
              Leave(time + randint(*customs.check_interval), i, car, customs)
          else:
              customs.enqueue(car)
 
class Leave(Event):
      def __init__(self, leave_time, gate_num, car, customs):
          Event.__init__(self, leave_time, customs)
          self.car = car
          self.gate_num = gate_num
          customs.add_event(self)
          
      def run(self):
          time, customs = self.time(), self.host()
          event_log(time, "car leave")
          customs.free_gate(self.gate_num)
          customs.car_count_1()
          customs.total_time_acc(time - self.car.arrive_time())
          if customs.has_queued_car():
              car = customs.next_car()
              i = customs.find_gate()
              event_log(time, "car check")
              customs.wait_time_acc(time - car.arrive_time())
              Leave(time + randint(*customs.check_interval), self.gate_num, car, customs)

if __name__ == '__main__':
    car_arrive_interval = (1,2)
    car_check_time = (3,5)
    cus = Customs(5, 480, car_arrive_interval, car_check_time)
    cus.simulate()
