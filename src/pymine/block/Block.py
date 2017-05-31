from src.pymine import block
from ..metadata.Metadatable import *
from ..level.Position import *
from ..event.block import *

class Block(__all__.BlockIds, Metadatable, Position):
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

            self.list[__all__.BlockIds.ACACIA_DOOR_BLOCK] = __all__.AcaciaDoor
#             self.list[__all__.BlockIds.AIR] = __all__.Air
#             self.list[__all__.BlockIds.STONE] = __all__.Stone
#             self.list[__all__.BlockIds.GRASS] = __all__.Grass
#             self.list[__all__.BlockIds.DIRT] = __all__.Dirt
#             self.list[__all__.BlockIds.COBBLESTONE] = __all__.Cobblestone
#             self.list[__all__.BlockIds.PLANKS] = __all__.Planks
#             self.list[__all__.BlockIds.SAPLING] = __all__.Sapling
#             self.list[__all__.BlockIds.BEDROCK] = __all__.Bedrock
#             self.list[__all__.BlockIds.WATER] = __all__.Water
#             self.list[__all__.BlockIds.STILL_WATER] = __all__.StillWater
#             self.list[__all__.BlockIds.LAVA] = __all__.Lava
#             self.list[__all__.BlockIds.STILL_LAVA] = __all__.StillLava
#             self.list[__all__.BlockIds.SAND] = __all__.Sand
#             self.list[__all__.BlockIds.GRAVEL] = __all__.Gravel
#             self.list[__all__.BlockIds.GOLD_ORE] = __all__.GoldOre
#             self.list[__all__.BlockIds.IRON_ORE] = __all__.IronOre
#             self.list[__all__.BlockIds.COAL_ORE] = __all__.CoalOre
#             self.list[__all__.BlockIds.WOOD] = __all__.Wood
#             self.list[__all__.BlockIds.LEAVES] = __all__.Leaves
#             self.list[__all__.BlockIds.SPONGE] = __all__.Sponge
#             self.list[__all__.BlockIds.GLASS] = __all__.Glass
#             self.list[__all__.BlockIds.LAPIS_ORE] = __all__.LapisOre
#             self.list[__all__.BlockIds.LAPIS_BLOCK] = __all__.Lapis
            self.list[__all__.BlockIds.ACTIVATOR_RAIL] = __all__.ActivatorRail
#             self.list[__all__.BlockIds.COCOA_BLOCK] = __all__.CocoaBlock
#             self.list[__all__.BlockIds.SANDSTONE] = __all__.Sandstone
#             self.list[__all__.BlockIds.NOTE_BLOCK] = __all__.NoteBlock
#             self.list[__all__.BlockIds.BED_BLOCK] = __all__.Bed
#             self.list[__all__.BlockIds.POWERED_RAIL] = __all__.PoweredRail
#             self.list[__all__.BlockIds.DETECTOR_RAIL] = __all__.DetectorRail
#             self.list[__all__.BlockIds.COBWEB] = __all__.Cobweb
#             self.list[__all__.BlockIds.TALL_GRASS] = __all__.TallGrass
#             self.list[__all__.BlockIds.DEAD_BUSH] = __all__.DeadBush
#             self.list[__all__.BlockIds.WOOL] = __all__.Wool
#             self.list[__all__.BlockIds.DANDELION] = __all__.Dandelion
#             self.list[__all__.BlockIds.RED_FLOWER] = __all__.Flower
#             self.list[__all__.BlockIds.BROWN_MUSHROOM] = __all__.BrownMushroom
#             self.list[__all__.BlockIds.RED_MUSHROOM] = __all__.RedMushroom
#             self.list[__all__.BlockIds.GOLD_BLOCK] = __all__.Gold
#             self.list[__all__.BlockIds.IRON_BLOCK] = __all__.Iron
#             self.list[__all__.BlockIds.DOUBLE_SLAB] = __all__.DoubleSlab
#             self.list[__all__.BlockIds.SLAB] = __all__.Slab
#             self.list[__all__.BlockIds.BRICKS_BLOCK] = __all__.Bricks
#             self.list[__all__.BlockIds.TNT] = __all__.TNT
#             self.list[__all__.BlockIds.BOOKSHELF] = __all__.Bookshelf
#             self.list[__all__.BlockIds.MOSS_STONE] = __all__.MossStone
#             self.list[__all__.BlockIds.OBSIDIAN] = __all__.Obsidian
#             self.list[__all__.BlockIds.TORCH] = __all__.Torch
#             self.list[__all__.BlockIds.FIRE] = __all__.Fire
#             self.list[__all__.BlockIds.MONSTER_SPAWNER] = __all__.MonsterSpawner
#             self.list[__all__.BlockIds.WOOD_STAIRS] = __all__.WoodStairs
#             self.list[__all__.BlockIds.CHEST] = __all__.Chest
# 
#             self.list[__all__.BlockIds.DIAMOND_ORE] = __all__.DiamondOre
#             self.list[__all__.BlockIds.DIAMOND_BLOCK] = __all__.Diamond
#             self.list[__all__.BlockIds.WORKBENCH] = __all__.Workbench
#             self.list[__all__.BlockIds.WHEAT_BLOCK] = __all__.Wheat
#             self.list[__all__.BlockIds.FARMLAND] = __all__.Farmland
#             self.list[__all__.BlockIds.FURNACE] = __all__.Furnace
#             self.list[__all__.BlockIds.BURNING_FURNACE] = __all__.BurningFurnace
#             self.list[__all__.BlockIds.SIGN_POST] = __all__.SignPost
#             self.list[__all__.BlockIds.WOOD_DOOR_BLOCK] = __all__.WoodDoor
#             self.list[__all__.BlockIds.SPRUCE_DOOR_BLOCK] = __all__.SpruceDoor
#             self.list[__all__.BlockIds.BIRCH_DOOR_BLOCK] = __all__.BirchDoor
#             self.list[__all__.BlockIds.JUNGLE_DOOR_BLOCK] = __all__.JungleDoor
#             self.list[__all__.BlockIds.DARK_OAK_DOOR_BLOCK] = __all__.DarkOakDoor
#             self.list[__all__.BlockIds.LADDER] = __all__.Ladder
#             self.list[__all__.BlockIds.RAIL] = __all__.Rail
# 
#             self.list[__all__.BlockIds.COBBLESTONE_STAIRS] = __all__.CobblestoneStairs
#             self.list[__all__.BlockIds.WALL_SIGN] = __all__.WallSign
#             self.list[__all__.BlockIds.LEVER] = __all__.Lever
#             self.list[__all__.BlockIds.STONE_PRESSURE_PLATE] = __all__.StonePressurePlate
#             self.list[__all__.BlockIds.IRON_DOOR_BLOCK] = __all__.IronDoor
#             self.list[__all__.BlockIds.WOODEN_PRESSURE_PLATE] = __all__.WoodenPressurePlate
#             self.list[__all__.BlockIds.REDSTONE_ORE] = __all__.RedstoneOre
#             self.list[__all__.BlockIds.GLOWING_REDSTONE_ORE] = __all__.GlowingRedstoneOre
# 
#             self.list[__all__.BlockIds.REDSTONE_TORCH] = __all__.RedstoneTorch
#             self.list[__all__.BlockIds.LIT_REDSTONE_TORCH] = __all__.LitRedstoneTorch
#             self.list[__all__.BlockIds.STONE_BUTTON] = __all__.StoneButton
#             self.list[__all__.BlockIds.SNOW_LAYER] = __all__.SnowLayer
#             self.list[__all__.BlockIds.ICE] = __all__.Ice
#             self.list[__all__.BlockIds.SNOW_BLOCK] = __all__.Snow
#             self.list[__all__.BlockIds.CACTUS] = __all__.Cactus
#             self.list[__all__.BlockIds.CLAY_BLOCK] = __all__.Clay
#             self.list[__all__.BlockIds.SUGARCANE_BLOCK] = __all__.Sugarcane
# 
#             self.list[__all__.BlockIds.FENCE] = __all__.Fence
#             self.list[__all__.BlockIds.PUMPKIN] = __all__.Pumpkin
#             self.list[__all__.BlockIds.NETHERRACK] = __all__.Netherrack
#             self.list[__all__.BlockIds.SOUL_SAND] = __all__.SoulSand
#             self.list[__all__.BlockIds.GLOWSTONE_BLOCK] = __all__.Glowstone
# 
#             self.list[__all__.BlockIds.LIT_PUMPKIN] = __all__.LitPumpkin
#             self.list[__all__.BlockIds.CAKE_BLOCK] = __all__.Cake
# 
#             self.list[__all__.BlockIds.TRAPDOOR] = __all__.Trapdoor
# 
#             self.list[__all__.BlockIds.STONE_BRICKS] = __all__.StoneBricks
# 
#             self.list[__all__.BlockIds.IRON_BARS] = __all__.IronBars
#             self.list[__all__.BlockIds.GLASS_PANE] = __all__.GlassPane
#             self.list[__all__.BlockIds.MELON_BLOCK] = __all__.Melon
#             self.list[__all__.BlockIds.PUMPKIN_STEM] = __all__.PumpkinStem
#             self.list[__all__.BlockIds.MELON_STEM] = __all__.MelonStem
#             self.list[__all__.BlockIds.VINE] = Vine
#             self.list[__all__.BlockIds.FENCE_GATE] = __all__.FenceGate
#             self.list[__all__.BlockIds.BRICK_STAIRS] = __all__.BrickStairs
#             self.list[__all__.BlockIds.STONE_BRICK_STAIRS] = __all__.StoneBrickStairs
# 
#             self.list[__all__.BlockIds.MYCELIUM] = __all__.Mycelium
#             self.list[__all__.BlockIds.WATER_LILY] = __all__.WaterLily
#             self.list[__all__.BlockIds.NETHER_BRICKS] = __all__.NetherBrick
#             self.list[__all__.BlockIds.NETHER_BRICK_FENCE] = __all__.NetherBrickFence
#             self.list[__all__.BlockIds.NETHER_BRICKS_STAIRS] = __all__.NetherBrickStairs
# 
#             self.list[__all__.BlockIds.ENCHANTING_TABLE] = __all__.EnchantingTable
#             self.list[__all__.BlockIds.BREWING_STAND_BLOCK] = __all__.BrewingStand
#             self.list[__all__.BlockIds.END_PORTAL] = __all__.EndPortal
#             self.list[__all__.BlockIds.END_PORTAL_FRAME] = __all__.EndPortalFrame
#             self.list[__all__.BlockIds.END_STONE] = __all__.EndStone
#             self.list[__all__.BlockIds.END_STONE_BRICKS] = __all__.EndStoneBricks
#             self.list[__all__.BlockIds.REDSTONE_LAMP] = __all__.RedstoneLamp
#             self.list[__all__.BlockIds.LIT_REDSTONE_LAMP] = __all__.LitRedstoneLamp
#             self.list[__all__.BlockIds.SANDSTONE_STAIRS] = __all__.SandstoneStairs
#             self.list[__all__.BlockIds.EMERALD_ORE] = __all__.EmeraldOre
#             self.list[__all__.BlockIds.ENDER_CHEST] = __all__.EnderChest
#             self.list[__all__.BlockIds.TRIPWIRE_HOOK] = __all__.TripwireHook
#             self.list[__all__.BlockIds.TRIPWIRE] = __all__.Tripwire
#             self.list[__all__.BlockIds.EMERALD_BLOCK] = __all__.Emerald
#             self.list[__all__.BlockIds.SPRUCE_WOOD_STAIRS] = __all__.SpruceWoodStairs
#             self.list[__all__.BlockIds.BIRCH_WOOD_STAIRS] = __all__.BirchWoodStairs
#             self.list[__all__.BlockIds.JUNGLE_WOOD_STAIRS] = __all__.JungleWoodStairs
#             self.list[__all__.BlockIds.BEACON] = __all__.Beacon
#             self.list[__all__.BlockIds.STONE_WALL] = __all__.StoneWall
#             self.list[__all__.BlockIds.FLOWER_POT_BLOCK] = __all__.FlowerPot
#             self.list[__all__.BlockIds.CARROT_BLOCK] = __all__.Carrot
#             self.list[__all__.BlockIds.POTATO_BLOCK] = __all__.Potato
#             self.list[__all__.BlockIds.WOODEN_BUTTON] = __all__.WoodenButton
#             self.list[__all__.BlockIds.MOB_HEAD_BLOCK] = __all__.MobHead
#             self.list[__all__.BlockIds.ANVIL] = __all__.Anvil
#             self.list[__all__.BlockIds.TRAPPED_CHEST] = __all__.TrappedChest
#             self.list[__all__.BlockIds.WEIGHTED_PRESSURE_PLATE_LIGHT] = __all__.WeightedPressurePlateLight
#             self.list[__all__.BlockIds.WEIGHTED_PRESSURE_PLATE_HEAVY] = __all__.WeightedPressurePlateHeavy
# 
#             self.list[__all__.BlockIds.DAYLIGHT_SENSOR] = __all__.DaylightSensor
#             self.list[__all__.BlockIds.REDSTONE_BLOCK] = __all__.Redstone
# 
#             self.list[__all__.BlockIds.COMMAND_BLOCK] = __all__.CommandBlock
#             self.list[__all__.BlockIds.QUARTZ_BLOCK] = __all__.Quartz
#             self.list[__all__.BlockIds.QUARTZ_STAIRS] = __all__.QuartzStairs
#             self.list[__all__.BlockIds.DOUBLE_WOOD_SLAB] = __all__.DoubleWoodSlab
#             self.list[__all__.BlockIds.WOOD_SLAB] = __all__.WoodSlab
#             self.list[__all__.BlockIds.STAINED_CLAY] = __all__.StainedClay
# 
#             self.list[__all__.BlockIds.LEAVES2] = __all__.Leaves2
#             self.list[__all__.BlockIds.WOOD2] = __all__.Wood2
#             self.list[__all__.BlockIds.ACACIA_WOOD_STAIRS] = __all__.AcaciaWoodStairs
#             self.list[__all__.BlockIds.DARK_OAK_WOOD_STAIRS] = __all__.DarkOakWoodStairs
#             self.list[__all__.BlockIds.PRISMARINE] = __all__.Prismarine
#             self.list[__all__.BlockIds.SEA_LANTERN] = __all__.SeaLantern
#             self.list[__all__.BlockIds.IRON_TRAPDOOR] = __all__.IronTrapdoor
#             self.list[__all__.BlockIds.HAY_BALE] = __all__.HayBale
#             self.list[__all__.BlockIds.CARPET] = __all__.Carpet
#             self.list[__all__.BlockIds.HARDENED_CLAY] = __all__.HardenedClay
#             self.list[__all__.BlockIds.COAL_BLOCK] = __all__.Coal
#             self.list[__all__.BlockIds.PACKED_ICE] = __all__.PackedIce
#             self.list[__all__.BlockIds.DOUBLE_PLANT] = __all__.DoublePlant
# 
#             self.list[__all__.BlockIds.FENCE_GATE_SPRUCE] = __all__.FenceGateSpruce
#             self.list[__all__.BlockIds.FENCE_GATE_BIRCH] = __all__.FenceGateBirch
#             self.list[__all__.BlockIds.FENCE_GATE_JUNGLE] = __all__.FenceGateJungle
#             self.list[__all__.BlockIds.FENCE_GATE_DARK_OAK] = __all__.FenceGateDarkOak
#             self.list[__all__.BlockIds.FENCE_GATE_ACACIA] = __all__.FenceGateAcacia
# 
#             self.list[__all__.BlockIds.ITEM_FRAME_BLOCK] = __all__.ItemFrame
# 
#             self.list[__all__.BlockIds.GRASS_PATH] = __all__.GrassPath
# 
#             self.list[__all__.BlockIds.PODZOL] = __all__.Podzol
#             self.list[__all__.BlockIds.BEETROOT_BLOCK] = __all__.Beetroot
#             self.list[__all__.BlockIds.STONECUTTER] = __all__.Stonecutter
#             self.list[__all__.BlockIds.GLOWING_OBSIDIAN] = __all__.GlowingObsidian
# 
#             self.list[__all__.BlockIds.HOPPER_BLOCK] = __all__.Hopper
#                 self.list[__all__.BlockIds.DRAGON_EGG] = __all__.DragonEgg
#             self.list[__all__.BlockIds.CHORUS_FLOWER] = __all__.ChorusFlower
#              self.list[__all__.BlockIds.CHORUS_PLANT] = __all__.ChorusPlant
#             self.list[__all__.BlockIds.INVISIBLE_BEDROCK] = __all__.InvisibleBedrock

            for id, clas in self.list:
                if clas is not None:
                    block = clas()
                    
                    data = 0
                    while data < 16:
                       self.fullList[(id << 4) | data] = clas(data)
                       data += 1
                    
                    self.solid[id] = block.isSolid()
                    self.transparent[id] = block.isTransparent()

    def get(self, id, meta=0, pos:Position=None):
        try:
            block = self.list[id]
            if block is not None:
                block = block(meta)
            else:
                block = __all__.UnknownBlock(id, meta)
        except RuntimeError:
            block = __all__.UnknownBlock(id, meta)