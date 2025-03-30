public class Pikachu extends Pokemon{
    public Pikachu(int hp, String name, Flyable flyable) {
        super(hp, name, flyable);
    }

    @Override
    public void attack(Pokemon target) { // LSP
        System.out.println(this.getName() + "이(가) " + target.getName() +"을 전기공격을 합니다");
    }
}
