public abstract class Pokemon {
    private int hp;
    private String name;
    public Flyable flyable;  // has-a

    public Pokemon(int hp, String name, Flyable flyable) {
        this.hp = hp;
        this.name = name;
        this.flyable = flyable;
    }

    public void performFlyable(){
        this.flyable.fly();
    }

    public void setFlyable(Flyable f){
        this.flyable = f;
    }

    public int getHp() {
        return hp;
    }

    public void setHp(int hp) {
        this.hp = hp;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    //public abstract void attack(Pikachu p);
    public abstract void attack(Pokemon p);
}
