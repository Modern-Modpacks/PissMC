package site.pissmc.discord;

import java.time.OffsetDateTime;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.jagrosh.discordipc.IPCClient;
import com.jagrosh.discordipc.IPCListener;
import com.jagrosh.discordipc.entities.Packet;
import com.jagrosh.discordipc.entities.RichPresence;
import com.jagrosh.discordipc.entities.User;
import site.modernmodpacks.pissmc.Loader;

public class RPCListener implements IPCListener {
    @Override
    public void onReady(IPCClient client) {
        client.sendRichPresence(
            new RichPresence.Builder()
            .setDetails("PissMC Powered")
            .setStartTimestamp(OffsetDateTime.now().toEpochSecond())
            .setLargeImage("logo", String.format("%d Mods loaded", Loader.getLoadedModIds().size()))
            .setButtons(new Gson().fromJson("[{\"label\":\"Get PissMC\", \"url\":\"https://pissmc.modernmodpacks.site\"}]", JsonArray.class))
            .build()
        );
    }

    @Override
    public void onPacketSent(IPCClient client, Packet packet) {}
    @Override
    public void onPacketReceived(IPCClient client, Packet packet) {}
    @Override
    public void onActivityJoin(IPCClient client, String secret) {}
    @Override
    public void onActivitySpectate(IPCClient client, String secret) {}
    @Override
    public void onActivityJoinRequest(IPCClient client, String secret, User user) {}
    @Override
    public void onClose(IPCClient client, JsonObject json) {}
    @Override
    public void onDisconnect(IPCClient client, Throwable t) {}
}
