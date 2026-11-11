class Student{
    String subject;
    String name;
    float marks;

    Student(){
        System.out.println("******");
        subject =  "English";
        name = "Aashish";
        marks = 5000f;
    }

    void displayDetails(){
        System.out.println(subject + " | " + name + " | " + marks);
    }
}

class Main{
    public static void main(String[] args){
        Student student1 = new Student();
        Student student2 = new Student();
        Student student3 = new Student();

        student1.displayDetails();
        student2.displayDetails();
        student3.displayDetails();
    }
}