class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent
        self.size = 1  # Initialize size to 1
        self.right_count = 0  # Initialize right_count to 0

    def update_size(self):
        self.size = 1
        if self.left:
            self.size += self.left.size
        if self.right:
            self.size += self.right.size

    def update_right_count(self):
        self.right_count = self.right.size if self.right else 0

class AugmentedBinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value, parent=None)
        current_node = self.root
        parent = None
        while current_node is not None:
            parent = current_node
            if value < current_node.value:
                current_node = current_node.left
            elif value == current_node.value:
                return 0
            else:
                current_node = current_node.right
        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        if parent:
            parent.update_size()  # Update the size of the parent node and its ancestors
            parent.update_right_count()

    def search(self, value):
        current_node = self.root
        while current_node is not None:
            if value == current_node.value:
                return current_node
            elif value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right
        print(value, )
        return None

    def remove(self, value):
        def find_node(node, value):
            if node is None:
                return None
            if value == node.value:
                print(value, "Removido")
                return node
            elif value < node.value:
                return find_node(node.left, value)
            else:
                return find_node(node.right, value)

        node_to_remove = find_node(self.root, value)
        if node_to_remove is None:
            print(value, "não está na árvore, não pode ser removido")
            return  # Value not found, ignore removal

        def remove_node(node):
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor_parent = node
                successor = node.left
                while successor.right is not None:
                    successor_parent = successor
                    successor = successor.right
                if successor_parent != node:
                    successor_parent.right = successor.left
                else:
                    successor_parent.left = successor.left
                node.value = successor.value
                return node

        if node_to_remove == self.root:
            new_root = remove_node(self.root)
            if new_root is not None:
                new_root.parent = None
            self.root = new_root
            self.update_counts(self.root)
        else:
            parent = None
            current_node = self.root
            while current_node != node_to_remove:
                parent = current_node
                if value < current_node.value:
                    current_node = current_node.left
                else:
                    current_node = current_node.right

            if value < parent.value:
                parent.left = remove_node(parent.left)
            else:
                parent.right = remove_node(parent.right)

            self.update_counts(parent)

    def update_counts(self, node):
        if node is None:
            return
        node.update_right_count()
        node.update_size()

    def count_nodes(self, node):
        if node is None:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)
    """"
    def enesimoElemento(self, n):
        
        Returns the n-th element (counting from 1) of the pre-order traversal of the BST.
        

        def pre_order(node):
            nonlocal count
            if node is None:
                return None
            count += 1
            if count == n:
                return node.value
            result = pre_order(node.left)
            if result is not None:
                return result
            return pre_order(node.right)

        count = 0
        return pre_order(self.root)
"""

    def enesimoElemento(self, n):

        def inorder(node):
            nonlocal count
            if node is None:
                return None
            result = inorder(node.left)
            if result is not None:
                return result
            count += 1
            if count == n:
                return node.value
            return inorder(node.right)

        count = 0
        return inorder(self.root)

    def position(self, value):
        def get_position(node, value):
            if node is None:
                return -1
            if value < node.value:
                return get_position(node.left, value)
            elif value == node.value:
                return (node.left.size if node.left else 0) + 1  # Adicionar 1 à posição
            else:
                right_position = get_position(node.right, value)
                if right_position == -1:
                    return -1
                return node.left.size + 1 + right_position

        return get_position(self.root, value)

    """def position(self, x):
        def pre_order(node, target, count):
            if node is None:
                return None
            if node.value == target:
                return count
            left_result = pre_order(node.left, target, count + 1)
            if left_result is not None:
                return left_result
            right_result = pre_order(node.right, target, count + (node.left.size if node.left else 0) + 1)
            if right_result is not None:
                return right_result
            return None

        return pre_order(self.root, x, 1)"""

    def isFull(self):
        """
        Verifica se a árvore é uma árvore binária cheia.
        Retorna True se for cheia, False caso contrário.
        """
        return self._isFull(self.root)

    def _isFull(self, node):
        """
        Função auxiliar para verificar se a subárvore enraizada em um determinado nó é uma árvore binária cheia.
        """
        if node is None:
            return True

        if node.left is None and node.right is None:
            return True

        if node.left is not None and node.right is not None:
            return self._isFull(node.left) and self._isFull(node.right)

        return False

    def isComplete(self):
        """
        Verifica se a árvore é uma árvore binária completa.
        Retorna True se for completa, False caso contrário.
        """
        if self.root is None:
            return False

        node_queue = [self.root]
        leaf_found = False

        while len(node_queue) > 0:
            current_node = node_queue.pop(0)

            if leaf_found and (current_node.left is not None or current_node.right is not None):
                return False

            if current_node.left is None:
                leaf_found = True
            else:
                node_queue.append(current_node.left)

            if current_node.right is None:
                leaf_found = True
            else:
                node_queue.append(current_node.right)

        return True

    def calculate_average(tree):
        def calculate_sum(node):
            if node is None:
                return 0
            return node.value + calculate_sum(node.left) + calculate_sum(node.right)

        total_sum = calculate_sum(tree.root)
        node_count = tree.count_nodes(tree.root)
        average = total_sum / node_count if node_count > 0 else 0
        return average

    def calculate_median(tree):
        def in_order_traversal(node, values):
            if node is None:
                return
            in_order_traversal(node.left, values)
            values.append(node.value)
            in_order_traversal(node.right, values)

        values = []
        in_order_traversal(tree.root, values)
        values.sort()
        node_count = len(values)

        if node_count % 2 == 0:
            mid_index = node_count // 2
            median = values[mid_index-1]
        else:
            mid_index = node_count // 2
            median = values[mid_index]

        return median

    def imprimir_preordem(self):
        def pre_order(node):
            if node is None:
                return
            print(node.value, end=" ")
            pre_order(node.left)
            pre_order(node.right)

        pre_order(self.root)
        print()

    def imprimir(self, s):
        if s == 1:
            self.imprimir_diagrama_barras(self.root, 0)
        elif s == 2:
            self.imprimir_aninhamento(self.root)
            print()

    def imprimir_diagrama_barras(self, node, n):
        if node is not None:
            for i in range(n):
                print("    ", end="")
            print(str(node.value) + "------------------")
            self.imprimir_diagrama_barras(node.left, n + 1)
            self.imprimir_diagrama_barras(node.right, n + 1)

    def imprimir_aninhamento(self, node):
        if node is not None:
            print("(" + str(node.value), end="")
            if node.left or node.right:
                print(" ", end="")
            self.imprimir_aninhamento(node.left)
            self.imprimir_aninhamento(node.right)
            print(")", end="")


def insert_numbers_from_file(tree, filename):
    with open(filename, 'r') as file:
        for line in file:
            numbers = line.strip().split()
            for number in numbers:
                tree.insert(int(number))

def process_operations_from_file(tree, filename):
    with open('arquivo2.txt', 'r') as file:
        for line in file:
            tokens = line.strip().split()
            operation = tokens[0]
            if operation == 'INSIRA':
                value = int(tokens[1])
                if 0 !=tree.insert(value):
                    print(value, "adicionado")
                else:
                    print(value, "já está na árvore, não pode ser inserido")
            elif operation == 'REMOVA':
                value = int(tokens[1])
                tree.remove(value)
            elif operation == 'POSICAO':
                value = int(tokens[1])
                position = tree.position(value)
                print(position)
                #print(f"A posição de {value} é {position}")
            elif operation == 'MEDIANA':
                median = tree.calculate_median()
                print(median)
                #print(f"A mediana é {median}")
            elif operation == 'MEDIA':
                average = tree.calculate_average()
                print(average)
                #print(f"A média é {average}")
            elif operation == 'BUSCAR':
                value = int(tokens[1])
                result = tree.search(value)
                if result is not None:
                    #print(f"{value} encontrado na árvore")
                    print("Chave encontrada")
                else:
                    #print(f"{value} não encontrado na árvore")
                    print("Chave não encontrada")

            elif operation == 'CHEIA':
                is_full = tree.isFull()
                if(is_full):
                    print("A árvore é cheia")
                else:
                    print("A árvore não é cheia")
                #print(f"A árvore está cheia: {is_full}")
            elif operation == 'COMPLETA':
                is_complete = tree.isComplete()
                if(is_complete):
                    print("A árvore é completa")
                else:
                    print("A árvore não é completa")

                #print(f"A árvore está completa: {is_complete}")
            elif operation == 'ENESIMO':
                n = int(tokens[1])
                enesimo = tree.enesimoElemento(n)
                print(enesimo)
                #print(f"O {n}-ésimo elemento é {enesimo}")
            elif operation == 'IMPRIMA':
                format_type = int(tokens[1])
                tree.imprimir(format_type)
            elif operation == 'PREORDEM':
                tree.imprimir_preordem()


# Instanciando a árvore
tree = AugmentedBinarySearchTree()
insert_numbers_from_file(tree, 'arquivo1.txt')
process_operations_from_file(tree, 'arquivo2.txt')
