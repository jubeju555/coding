import java.util.Scanner;

class ArrayPractice {
    public static int findMin (int[] nums){
        int currentMin = nums[0];
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] < currentMin) {
            currentMin = nums[i];
            }
        }           
         return currentMin;

    }
    public static int findMax (int[] nums){
        int currentMax = nums[0];
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] > currentMax) {
            currentMax = nums[i];
            }
        }           
         return currentMax;
    }    
    public static int count0occurances (int[] nums, int value){
       int counter = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] == value) {
            counter ++;
            }
        }   
        return 0;
    }
    public static void main( String[] args){
        Scanner s = new Scanner(System.in);

        System.out.print("what is the size of the array?");
        int size = s.nextInt();
        int[] arr = new int[size];

        System.out.print("what are the elements ");
        for (int i = 0; i < size; i++) {
            System.out.println("Element " + i + ";");
            int val = s.nextInt();
            arr[i] = val;
        
        }
        s.close();
            System.out.println(" the minimum is " + findMin(arr));
            System.out.println(" the maximum is " + findMax(arr));
            System.out.println("the number of perferct scores is " + count0occurances(arr, 100));
            
    }

}