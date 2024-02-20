package site.pissmc.sprint;

import org.lwjgl.input.Keyboard;

import com.mojang.rubydung.Player;
import com.mojang.rubydung.RubyDung;
import site.modernmodpacks.pissmc.event.Event;
import site.modernmodpacks.pissmc.Loader;

public class Sprint {
    public Sprint() {
        Loader.addEventHandler(Event.POST_PLAYER_TICK, e -> {
            Player player = RubyDung.getInstance().getPlayer();
            if ((Keyboard.isKeyDown(Keyboard.KEY_LSHIFT) || Keyboard.isKeyDown(Keyboard.KEY_RSHIFT)) && player.onGround) player.moveRelative(player.xa, player.ya, 0.1F);
        });
    }
}