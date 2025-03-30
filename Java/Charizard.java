public class Charizard extends Pokemon{
    public Charizard(int hp, String name, Flyable flyable) {
        super(hp, name, flyable);
    }


    @Override
    public void attack(Pokemon target) {
        System.out.println(this.getName() + "이(가) " + target.getName() +"을 화염공격을 합니다");;
    }
}
