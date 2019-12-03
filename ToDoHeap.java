import java.util.HashSet;
import java.util.Scanner;

// An interactive program that stores to-do items in a heap with priority
// chosen by the user such that the user makes as few decisions as possible
class ToDoHeap {
	private static final int MIN_ARRAY_SIZE = 8;
	private Heap heap;
	private final String heapName;

	private ToDoHeap(String name) {
		heap = new Heap();
		heapName = name;
	}

	// Add an item to the heap
	private void add(String name) {	heap.add(new Item(name)); }

	// Display the item at the top of the heap
	private void peek() {
		String name = heap.peek();
		if (name == null) System.out.println("Heap is empty.");
		else System.out.println(name);
	}

	// Delete the item at the top of the heap
	private void delete() { heap.delete(); }

	// Display the entire heap
	private void view_tree() { heap.display(); }

	// Construct a heap from a text file
	private void constructHeap(String path) {}

	// Store a heap as a text file.
	private void storeHeap() {}

	// Display a list of all available commands.
	private void help() {
		// Commands:
		// new [name], open [name], heaps, save?, quit
		// add, delete ([item]), reorder?, moveToTop?
		// peek, viewtree
	}

	// An item in the heap that stores its name and all items of lower priority.
	private static class Item {
		public final String name;
		public final HashSet<Item> lowerPriority;

		public Item(String name) {
			this.name = name;
			lowerPriority = new HashSet<>();
		}
	}

	// Heap data structure supporting all required operations, implemented with
	// a resizing array.
	private static class Heap {
		private Item[] heapArray;
		private int N;

		// Construct an empty heap
		public Heap() {
			heapArray = new Item[MIN_ARRAY_SIZE];
			N = 0;
		}

		// Add an item to the heap
		public void add(Item item) {
			if (N == heapArray.length) resize(N << 1);
			heapArray[N] = item;
			siftUp(N++);
		}

		// Delete the item at the top of the heap
		public void delete() {
			if (N == 0) return;
			heapArray[0] = heapArray[--N];
			heapArray[N] = null;
			int len = heapArray.length;
			if (len > MIN_ARRAY_SIZE && N <= (len >> 2)) resize(len >> 1);
			siftDown(0);
		}

		// Return the name of the item at the top of the heap
		public String peek() {
			if (N == 0) return null;
			return heapArray[0].name;
		}

		// Print the heap in a nicely formatted style
		public void display() {}

		private void display(int i, boolean isLastChild) {}

		// Sift up from the given index
		private void siftUp(int i) {
			if (i == 0) return;
			int j = parent(i);
			Item item = heapArray[i];
			Item parent = heapArray[j];
			if (isHigher(parent, item)) return;
			swap(i, j);
			siftUp(j);
		}

		// Sift down from the given index
		private void siftDown(int i) {
			int j = left(i);
			if (j >= N) return;
			Item item = heapArray[i];
			Item leftChild = heapArray[j];
			if (isHigher(item, leftChild)) {
				if (j == N - 1) return;
				int k = right(i);
				Item rightChild = heapArray[k];
				if (isHigher(item, rightChild)) return;
				swap(i, k);
				siftDown(k);
				return;
			}
			if (j == N - 1) {
				swap(i, j);
				siftDown(j);
				return;
			}
			int k = right(i);
			Item rightChild = heapArray[k];
			if (isHigher(item, rightChild) || isHigher(leftChild, rightChild)) {
				swap(i, j);
				siftDown(j);
				return;
			}
			swap(i, k);
			siftDown(k);
		}

		// Is item A of higher priority than item B?  If the two items are not
		// comparable, their relative priority is determined by the user.
		private boolean isHigher(Item A, Item B) {
			if (A.lowerPriority.contains(B)) return true;
			if (B.lowerPriority.contains(A)) return false;
			Item X = query(A, B);
			Item Y = (X == A) ? B : A;
			setHigher(X, Y);
			return (X == A);
		}

		// Set the priority of item A to be higher than that of item B
		private void setHigher(Item A, Item B) {
			A.lowerPriority.add(B);
			for (Item X : B.lowerPriority) A.lowerPriority.add(X);
		}

		// Resize the heap array
		private void resize(int size) {
			Item[] copy = new Item[size];
			for (int i = 0; i < heapArray.length; i++) copy[i] = heapArray[i];
			heapArray = copy;
		}

		// Swap the positions of two items in the heap array
		private void swap(int i, int j) {
			Item temp = heapArray[i];
			heapArray[i] = heapArray[j];
			heapArray[j] = temp;
		}
	}

	// Ask the user to select the item of greater priority
	private static Item query(Item A, Item B) {
		Scanner input = new Scanner(System.in);
		Item X;
		while (true) {
			System.out.println("Select the item of higher priority:");
			System.out.println("1: " + A.name);
			System.out.println("2: " + B.name);
			String s = input.nextLine();
			if (s.length() == 0) continue;
			char c = s.charAt(0);
			if (c == '1') X = A;
			else if (c == '2') X = B;
			else continue;
			System.out.println("You selected: " + X.name);
			break;
		}
		return X;
	}

	// Index of parent node in array
	private static int parent(int i) { return (i - 1) >> 1; }

	// Index of left child node in array
	private static int left(int i) { return (i << 1) + 1; }

	// Index of right child node in array
	private static int right(int i) { return (i << 1) + 2; }

	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		System.out.println("Enter heap name");
		String heapName = input.nextLine();
		ToDoHeap heap = new ToDoHeap(heapName);
		while (true) {
			System.out.println("What would you like to do?");
			String command = input.nextLine();
			if (command.equals("add")) {
				System.out.println("Enter name of item to add:");
				String name = input.nextLine();
				heap.add(name);
			} else if (command.equals("delete") heap.delete();
			else if (command.equals("quit")) break;
		}
	}
}
