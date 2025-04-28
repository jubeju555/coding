import java.util.ArrayList;

class Arraylistpractice {
    public static void main (String[] args){
            System.out.println("hi");
        ArrayList<Integer> scores = new ArrayList<Integer>();
        scores.add(100);
        scores.add(200);

        for (int i = 0; i < scores.size(); i++) {
            System.out.println(scores.get(i));
        }

    }
    
}

