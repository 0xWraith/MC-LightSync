package ru.wraith.mcsync;

import org.bukkit.Location;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;


public class Main extends JavaPlugin implements Listener
{
	
	@Override
    public void onEnable() {
		System.out.println("mc-sync plugin started!");
    }
    @Override
    public void onDisable() {
    	System.out.println("mc-sync plugin disabled!");
    }
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) 
    {
    	if(args.length != 1)
    	{
    		sender.sendMessage("E0: Invalid number of arguments!");
    		System.out.println("E0: Invalid number of arguments!");
    		
    		return true;
    	}
    	
    	Player player = getServer().getPlayer(args[0]);
    	
    	if(player == null)
    	{
    		sender.sendMessage("E1: Invalid player nickname!");
    		System.out.println("E1: Invalid player nickname!");
    		
    		return true;
    	}
    	System.out.println(sender);
    	Location headPos = player.getEyeLocation();
    	int lightLVL = headPos.getBlock().getLightLevel();
    	sender.sendMessage(String.valueOf(lightLVL));
    	
    	return false;
    }
}
