import javax.print.attribute.standard.JobKOctets;

public class PokemonGame {
    public static void main(String[] args) {
        //Pokemon pokemon = new Pokemon(100, 1);
        Charizard charizard1 = new Charizard(300, "나쁜리자몽", new Wings());
        Charizard charizard2 = new Charizard(300, "착한리자몽", new Wings());
        Pikachu pikachu = new Pikachu(99, "지우피카츄", new NoFly());

        pikachu.attack(charizard1);
        charizard2.performFlyable();
        pikachu.performFlyable();
        JetPack jetPack = new JetPack();
        pikachu.setFlyable(jetPack);
        pikachu.performFlyable();
    }
}
