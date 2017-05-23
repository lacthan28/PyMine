from pymine.block import BlockIds, AcaciaDoor
from pymine.metadata import Metadatable
from pymine.level import Position
from pymine.event import block
from aifc import data

class Block(BlockIds, Metadatable, Position):
    list = None
    fullList = None
    light = None
    ligthFilter = None
    solid = None
    hardness = None
    transparent = None
    
    id = None
    meta = 0
    
    boundingBox = None
    
    def __init__(self):
        if self.list is None:
            self.list = []
            self.fullList = []
            self.light = []
            self.ligthFilter = []
            self.solid = []
            self.hardness = []
            self.transparent = []
            
            self.list[BlockIds.ACACIA_DOOR_BLOCK] = AcaciaDoor.AcaciaDoor.__class__        
#             self.list[BlockIds.AIR] = Air.__class__;
#             self.list[BlockIds.STONE] = Stone.__class__;
#             self.list[BlockIds.GRASS] = Grass.__class__;
#             self.list[BlockIds.DIRT] = Dirt.__class__;
#             self.list[BlockIds.COBBLESTONE] = Cobblestone.__class__;
#             self.list[BlockIds.PLANKS] = Planks.__class__;
#             self.list[BlockIds.SAPLING] = Sapling.__class__;
#             self.list[BlockIds.BEDROCK] = Bedrock.__class__;
#             self.list[BlockIds.WATER] = Water.__class__;
#             self.list[BlockIds.STILL_WATER] = StillWater.__class__;
#             self.list[BlockIds.LAVA] = Lava.__class__;
#             self.list[BlockIds.STILL_LAVA] = StillLava.__class__;
#             self.list[BlockIds.SAND] = Sand.__class__;
#             self.list[BlockIds.GRAVEL] = Gravel.__class__;
#             self.list[BlockIds.GOLD_ORE] = GoldOre.__class__;
#             self.list[BlockIds.IRON_ORE] = IronOre.__class__;
#             self.list[BlockIds.COAL_ORE] = CoalOre.__class__;
#             self.list[BlockIds.WOOD] = Wood.__class__;
#             self.list[BlockIds.LEAVES] = Leaves.__class__;
#             self.list[BlockIds.SPONGE] = Sponge.__class__;
#             self.list[BlockIds.GLASS] = Glass.__class__;
#             self.list[BlockIds.LAPIS_ORE] = LapisOre.__class__;
#             self.list[BlockIds.LAPIS_BLOCK] = Lapis.__class__;
#             self.list[BlockIds.ACTIVATOR_RAIL] = ActivatorRail.__class__;
#             self.list[BlockIds.COCOA_BLOCK] = CocoaBlock.__class__;
#             self.list[BlockIds.SANDSTONE] = Sandstone.__class__;
#             self.list[BlockIds.NOTE_BLOCK] = NoteBlock.__class__;
#             self.list[BlockIds.BED_BLOCK] = Bed.__class__;
#             self.list[BlockIds.POWERED_RAIL] = PoweredRail.__class__;
#             self.list[BlockIds.DETECTOR_RAIL] = DetectorRail.__class__;
#             self.list[BlockIds.COBWEB] = Cobweb.__class__;
#             self.list[BlockIds.TALL_GRASS] = TallGrass.__class__;
#             self.list[BlockIds.DEAD_BUSH] = DeadBush.__class__;
#             self.list[BlockIds.WOOL] = Wool.__class__;
#             self.list[BlockIds.DANDELION] = Dandelion.__class__;
#             self.list[BlockIds.RED_FLOWER] = Flower.__class__;
#             self.list[BlockIds.BROWN_MUSHROOM] = BrownMushroom.__class__;
#             self.list[BlockIds.RED_MUSHROOM] = RedMushroom.__class__;
#             self.list[BlockIds.GOLD_BLOCK] = Gold.__class__;
#             self.list[BlockIds.IRON_BLOCK] = Iron.__class__;
#             self.list[BlockIds.DOUBLE_SLAB] = DoubleSlab.__class__;
#             self.list[BlockIds.SLAB] = Slab.__class__;
#             self.list[BlockIds.BRICKS_BLOCK] = Bricks.__class__;
#             self.list[BlockIds.TNT] = TNT.__class__;
#             self.list[BlockIds.BOOKSHELF] = Bookshelf.__class__;
#             self.list[BlockIds.MOSS_STONE] = MossStone.__class__;
#             self.list[BlockIds.OBSIDIAN] = Obsidian.__class__;
#             self.list[BlockIds.TORCH] = Torch.__class__;
#             self.list[BlockIds.FIRE] = Fire.__class__;
#             self.list[BlockIds.MONSTER_SPAWNER] = MonsterSpawner.__class__;
#             self.list[BlockIds.WOOD_STAIRS] = WoodStairs.__class__;
#             self.list[BlockIds.CHEST] = Chest.__class__;
# 
#             self.list[BlockIds.DIAMOND_ORE] = DiamondOre.__class__;
#             self.list[BlockIds.DIAMOND_BLOCK] = Diamond.__class__;
#             self.list[BlockIds.WORKBENCH] = Workbench.__class__;
#             self.list[BlockIds.WHEAT_BLOCK] = Wheat.__class__;
#             self.list[BlockIds.FARMLAND] = Farmland.__class__;
#             self.list[BlockIds.FURNACE] = Furnace.__class__;
#             self.list[BlockIds.BURNING_FURNACE] = BurningFurnace.__class__;
#             self.list[BlockIds.SIGN_POST] = SignPost.__class__;
#             self.list[BlockIds.WOOD_DOOR_BLOCK] = WoodDoor.__class__;
#             self.list[BlockIds.SPRUCE_DOOR_BLOCK] = SpruceDoor.__class__;
#             self.list[BlockIds.BIRCH_DOOR_BLOCK] = BirchDoor.__class__;
#             self.list[BlockIds.JUNGLE_DOOR_BLOCK] = JungleDoor.__class__;
#             self.list[BlockIds.ACACIA_DOOR_BLOCK] = AcaciaDoor.__class__;
#             self.list[BlockIds.DARK_OAK_DOOR_BLOCK] = DarkOakDoor.__class__;
#             self.list[BlockIds.LADDER] = Ladder.__class__;
#             self.list[BlockIds.RAIL] = Rail.__class__;
# 
#             self.list[BlockIds.COBBLESTONE_STAIRS] = CobblestoneStairs.__class__;
#             self.list[BlockIds.WALL_SIGN] = WallSign.__class__;
#             self.list[BlockIds.LEVER] = Lever.__class__;
#             self.list[BlockIds.STONE_PRESSURE_PLATE] = StonePressurePlate.__class__;
#             self.list[BlockIds.IRON_DOOR_BLOCK] = IronDoor.__class__;
#             self.list[BlockIds.WOODEN_PRESSURE_PLATE] = WoodenPressurePlate.__class__;
#             self.list[BlockIds.REDSTONE_ORE] = RedstoneOre.__class__;
#             self.list[BlockIds.GLOWING_REDSTONE_ORE] = GlowingRedstoneOre.__class__;
# 
#             self.list[BlockIds.REDSTONE_TORCH] = RedstoneTorch.__class__;
#             self.list[BlockIds.LIT_REDSTONE_TORCH] = LitRedstoneTorch.__class__;
#             self.list[BlockIds.STONE_BUTTON] = StoneButton.__class__;
#             self.list[BlockIds.SNOW_LAYER] = SnowLayer.__class__;
#             self.list[BlockIds.ICE] = Ice.__class__;
#             self.list[BlockIds.SNOW_BLOCK] = Snow.__class__;
#             self.list[BlockIds.CACTUS] = Cactus.__class__;
#             self.list[BlockIds.CLAY_BLOCK] = Clay.__class__;
#             self.list[BlockIds.SUGARCANE_BLOCK] = Sugarcane.__class__;
# 
#             self.list[BlockIds.FENCE] = Fence.__class__;
#             self.list[BlockIds.PUMPKIN] = Pumpkin.__class__;
#             self.list[BlockIds.NETHERRACK] = Netherrack.__class__;
#             self.list[BlockIds.SOUL_SAND] = SoulSand.__class__;
#             self.list[BlockIds.GLOWSTONE_BLOCK] = Glowstone.__class__;
# 
#             self.list[BlockIds.LIT_PUMPKIN] = LitPumpkin.__class__;
#             self.list[BlockIds.CAKE_BLOCK] = Cake.__class__;
# 
#             self.list[BlockIds.TRAPDOOR] = Trapdoor.__class__;
# 
#             self.list[BlockIds.STONE_BRICKS] = StoneBricks.__class__;
# 
#             self.list[BlockIds.IRON_BARS] = IronBars.__class__;
#             self.list[BlockIds.GLASS_PANE] = GlassPane.__class__;
#             self.list[BlockIds.MELON_BLOCK] = Melon.__class__;
#             self.list[BlockIds.PUMPKIN_STEM] = PumpkinStem.__class__;
#             self.list[BlockIds.MELON_STEM] = MelonStem.__class__;
#             self.list[BlockIds.VINE] = Vine.__class__;
#             self.list[BlockIds.FENCE_GATE] = FenceGate.__class__;
#             self.list[BlockIds.BRICK_STAIRS] = BrickStairs.__class__;
#             self.list[BlockIds.STONE_BRICK_STAIRS] = StoneBrickStairs.__class__;
# 
#             self.list[BlockIds.MYCELIUM] = Mycelium.__class__;
#             self.list[BlockIds.WATER_LILY] = WaterLily.__class__;
#             self.list[BlockIds.NETHER_BRICKS] = NetherBrick.__class__;
#             self.list[BlockIds.NETHER_BRICK_FENCE] = NetherBrickFence.__class__;
#             self.list[BlockIds.NETHER_BRICKS_STAIRS] = NetherBrickStairs.__class__;
# 
#             self.list[BlockIds.ENCHANTING_TABLE] = EnchantingTable.__class__;
#             self.list[BlockIds.BREWING_STAND_BLOCK] = BrewingStand.__class__;
#             self.list[BlockIds.END_PORTAL] = EndPortal.__class__;
#             self.list[BlockIds.END_PORTAL_FRAME] = EndPortalFrame.__class__;
#             self.list[BlockIds.END_STONE] = EndStone.__class__;
#             self.list[BlockIds.END_STONE_BRICKS] = EndStoneBricks.__class__;
#             self.list[BlockIds.REDSTONE_LAMP] = RedstoneLamp.__class__;
#             self.list[BlockIds.LIT_REDSTONE_LAMP] = LitRedstoneLamp.__class__;
#             self.list[BlockIds.SANDSTONE_STAIRS] = SandstoneStairs.__class__;
#             self.list[BlockIds.EMERALD_ORE] = EmeraldOre.__class__;
#             self.list[BlockIds.ENDER_CHEST] = EnderChest.__class__;
#             self.list[BlockIds.TRIPWIRE_HOOK] = TripwireHook.__class__;
#             self.list[BlockIds.TRIPWIRE] = Tripwire.__class__;
#             self.list[BlockIds.EMERALD_BLOCK] = Emerald.__class__;
#             self.list[BlockIds.SPRUCE_WOOD_STAIRS] = SpruceWoodStairs.__class__;
#             self.list[BlockIds.BIRCH_WOOD_STAIRS] = BirchWoodStairs.__class__;
#             self.list[BlockIds.JUNGLE_WOOD_STAIRS] = JungleWoodStairs.__class__;
#             self.list[BlockIds.BEACON] = Beacon.__class__;
#             self.list[BlockIds.STONE_WALL] = StoneWall.__class__;
#             self.list[BlockIds.FLOWER_POT_BLOCK] = FlowerPot.__class__;
#             self.list[BlockIds.CARROT_BLOCK] = Carrot.__class__;
#             self.list[BlockIds.POTATO_BLOCK] = Potato.__class__;
#             self.list[BlockIds.WOODEN_BUTTON] = WoodenButton.__class__;
#             self.list[BlockIds.MOB_HEAD_BLOCK] = MobHead.__class__;
#             self.list[BlockIds.ANVIL] = Anvil.__class__;
#             self.list[BlockIds.TRAPPED_CHEST] = TrappedChest.__class__;
#             self.list[BlockIds.WEIGHTED_PRESSURE_PLATE_LIGHT] = WeightedPressurePlateLight.__class__;
#             self.list[BlockIds.WEIGHTED_PRESSURE_PLATE_HEAVY] = WeightedPressurePlateHeavy.__class__;
# 
#             self.list[BlockIds.DAYLIGHT_SENSOR] = DaylightSensor.__class__;
#             self.list[BlockIds.REDSTONE_BLOCK] = Redstone.__class__;
# 
#             self.list[BlockIds.COMMAND_BLOCK] = CommandBlock.__class__;
#             self.list[BlockIds.QUARTZ_BLOCK] = Quartz.__class__;
#             self.list[BlockIds.QUARTZ_STAIRS] = QuartzStairs.__class__;
#             self.list[BlockIds.DOUBLE_WOOD_SLAB] = DoubleWoodSlab.__class__;
#             self.list[BlockIds.WOOD_SLAB] = WoodSlab.__class__;
#             self.list[BlockIds.STAINED_CLAY] = StainedClay.__class__;
# 
#             self.list[BlockIds.LEAVES2] = Leaves2.__class__;
#             self.list[BlockIds.WOOD2] = Wood2.__class__;
#             self.list[BlockIds.ACACIA_WOOD_STAIRS] = AcaciaWoodStairs.__class__;
#             self.list[BlockIds.DARK_OAK_WOOD_STAIRS] = DarkOakWoodStairs.__class__;
#             self.list[BlockIds.PRISMARINE] = Prismarine.__class__;
#             self.list[BlockIds.SEA_LANTERN] = SeaLantern.__class__;
#             self.list[BlockIds.IRON_TRAPDOOR] = IronTrapdoor.__class__;
#             self.list[BlockIds.HAY_BALE] = HayBale.__class__;
#             self.list[BlockIds.CARPET] = Carpet.__class__;
#             self.list[BlockIds.HARDENED_CLAY] = HardenedClay.__class__;
#             self.list[BlockIds.COAL_BLOCK] = Coal.__class__;
#             self.list[BlockIds.PACKED_ICE] = PackedIce.__class__;
#             self.list[BlockIds.DOUBLE_PLANT] = DoublePlant.__class__;
# 
#             self.list[BlockIds.FENCE_GATE_SPRUCE] = FenceGateSpruce.__class__;
#             self.list[BlockIds.FENCE_GATE_BIRCH] = FenceGateBirch.__class__;
#             self.list[BlockIds.FENCE_GATE_JUNGLE] = FenceGateJungle.__class__;
#             self.list[BlockIds.FENCE_GATE_DARK_OAK] = FenceGateDarkOak.__class__;
#             self.list[BlockIds.FENCE_GATE_ACACIA] = FenceGateAcacia.__class__;
# 
#             self.list[BlockIds.ITEM_FRAME_BLOCK] = ItemFrame.__class__;
# 
#             self.list[BlockIds.GRASS_PATH] = GrassPath.__class__;
# 
#             self.list[BlockIds.PODZOL] = Podzol.__class__;
#             self.list[BlockIds.BEETROOT_BLOCK] = Beetroot.__class__;
#             self.list[BlockIds.STONECUTTER] = Stonecutter.__class__;
#             self.list[BlockIds.GLOWING_OBSIDIAN] = GlowingObsidian.__class__;
# 
#             self.list[BlockIds.HOPPER_BLOCK] = Hopper.__class__;
#                 self.list[BlockIds.DRAGON_EGG] = DragonEgg.__class__;
#             self.list[BlockIds.CHORUS_FLOWER] = ChorusFlower.__class__;
#              self.list[BlockIds.CHORUS_PLANT] = ChorusPlant.__class__;
#             self.list[BlockIds.INVISIBLE_BEDROCK] = InvisibleBedrock.__class__;

            for id, clas in self.list:
                if clas is not None:
                    block = clas()
                    
                    data = 0
                    while data < 16:
                       self.fullList[(id << 4) | data] = clas(data)
                       data += 1
                    
#                     self.solid[id] = block.is