package site.pissmc.discord;

import com.jagrosh.discordipc.IPCClient;
import com.jagrosh.discordipc.exceptions.NoDiscordClientException;

public class DiscordRPC {
    @SuppressWarnings("resource")
    public DiscordRPC() throws NoDiscordClientException, InterruptedException{
        IPCClient client = new IPCClient(1157302967054114947L);
        client.setListener(new RPCListener());
        client.connect();
    }
}