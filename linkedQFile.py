class Node:

    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedQ:

    def __init__(self):
        self.__first = None
        self.__last = None

    def __str__(self):
        queue_chain = ""
        while self.__first:
            queue_chain += str(self.__first.value)
            self.__first = self.__first.next
        return queue_chain

    def enqueue(self, card):
        new_node = Node(card)
        if self.__first is None:
            self.__first = self.__last = new_node # initierar det främre och bakre kortet

        else: # Uppdaterar vi det bakre kortet
            self.__last.next = new_node
            self.__last = new_node

    def peek(self):
        if self.__first:
            return self.__first.value
        return None

    def isEmpty(self):
        if self.__first is None:
            return True
        return False

    def dequeue(self):
        card_to_remove = self.__first
        self.__first = self.__first.next

        return card_to_remove.value

