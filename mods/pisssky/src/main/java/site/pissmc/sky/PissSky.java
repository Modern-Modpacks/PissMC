package site.pissmc.sky;

import com.mojang.rubydung.RubyDung;

public class PissSky {
    public PissSky() {
        RubyDung instance = RubyDung.getInstance();
        instance.fr = 1;
        instance.fg = 0.96F;
        instance.fb = 0.29F;
    }
}