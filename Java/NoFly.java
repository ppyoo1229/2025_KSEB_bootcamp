public class NoFly implements Flyable{
    @Override
    public void fly() {
        System.out.println("하늘을 날수 없습니다!");
    }
}
