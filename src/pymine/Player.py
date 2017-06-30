class Player:
	SURVIVAL = 0

	CREATIVE = 1

	ADVENTURE = 2

	SPECTATOR = 3

	VIEW = SPECTATOR

	CRAFTING_SMALL = 0

	CRAFTING_BIG = 1

	CRAFTING_ANVIL = 2

	CRAFTING_ENCHANT = 3

	interface = None

	def dataPacket(self, packet: DataPacket):
		pass
