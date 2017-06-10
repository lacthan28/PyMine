from .Air import *
from .BlockIds import *
from .Liquid import *
from ..Player import *
from ..block import *
from ..entity.Entity import *
from ..item.Item import *
from ..level.Position import *
from ..maths.Vector3 import *
from ..metadata.Metadatable import *


class Block(BlockIds, Metadatable, Position):
    list = None
    fullList = None
    light = None
    lightFilter = None
    solid = None
    hardness = None
    transparent = None

    id = None
    meta = 0

    boundingBox = None

    def init(self):
        if self.list is None:
            self.list = FixedDict(256)
            self.fullList = []
            self.light = []
            self.lightFilter = []
            self.solid = []
            self.hardness = []
            self.transparent = []

            self.list[self.ACACIA_DOOR_BLOCK] = AcaciaDoor
            list = {
                self.ACACIA_DOOR_BLOCK: AcaciaDoor,
                self.AIR: Air,
                self.STONE: Stone,
                self.GRASS: Grass,
                self.DIRT: Dirt,
                self.COBBLESTONE: Cobblestone,
                self.PLANKS: Planks,
                self.SAPLING: Sapling,
                self.BEDROCK: Bedrock,
                self.WATER: Water,
                self.STILL_WATER: StillWater,
                self.LAVA: Lava,
                self.STILL_LAVA: StillLava,
                self.SAND: Sand,
                self.GRAVEL: Gravel,
                self.GOLD_ORE: GoldOre,
                self.IRON_ORE: IronOre,
                self.COAL_ORE: CoalOre,
                self.WOOD: Wood,
                self.LEAVES: Leaves,
                self.SPONGE: Sponge,
                self.GLASS: Glass,
                self.LAPIS_ORE: LapisOre,
                self.LAPIS_BLOCK: Lapis,
                self.ACTIVATOR_RAIL: ActivatorRail,
                self.COCOA_BLOCK: CocoaBlock,
                self.SANDSTONE: Sandstone,
                self.NOTE_BLOCK: NoteBlock,
                self.BED_BLOCK: Bed,
                self.POWERED_RAIL: PoweredRail,
                self.DETECTOR_RAIL: DetectorRail,
                self.COBWEB: Cobweb,
                self.TALL_GRASS: TallGrass,
                self.DEAD_BUSH: DeadBush,
                self.WOOL: Wool,
                self.DANDELION: Dandelion,
                self.RED_FLOWER: Flower,
                self.BROWN_MUSHROOM: BrownMushroom,
                self.RED_MUSHROOM: RedMushroom,
                self.GOLD_BLOCK: Gold,
                self.IRON_BLOCK: Iron,
                self.DOUBLE_SLAB: DoubleSlab,
                self.SLAB: Slab,
                self.BRICKS_BLOCK: Bricks,
                self.TNT: TNT,
                self.BOOKSHELF: Bookshelf,
                self.MOSS_STONE: MossStone,
                self.OBSIDIAN: Obsidian,
                self.TORCH: Torch,
                self.FIRE: Fire,
                self.MONSTER_SPAWNER: MonsterSpawner,
                self.WOOD_STAIRS: WoodStairs,
                self.CHEST: Chest,
                self.DIAMOND_ORE: DiamondOre,
                self.DIAMOND_BLOCK: Diamond,
                self.WORKBENCH: Workbench,
                self.WHEAT_BLOCK: Wheat,
                self.FARMLAND: Farmland,
                self.FURNACE: Furnace,
                self.BURNING_FURNACE: BurningFurnace,
                self.SIGN_POST: SignPost,
                self.WOOD_DOOR_BLOCK: WoodDoor,
                self.SPRUCE_DOOR_BLOCK: SpruceDoor,
                self.BIRCH_DOOR_BLOCK: BirchDoor,
                self.JUNGLE_DOOR_BLOCK: JungleDoor,
                self.DARK_OAK_DOOR_BLOCK: DarkOakDoor,
                self.LADDER: Ladder,
                self.RAIL: Rail,
                self.COBBLESTONE_STAIRS: CobblestoneStairs,
                self.WALL_SIGN: WallSign,
                self.LEVER: Lever,
                self.STONE_PRESSURE_PLATE: StonePressurePlate,
                self.IRON_DOOR_BLOCK: IronDoor,
                self.WOODEN_PRESSURE_PLATE: WoodenPressurePlate,
                self.REDSTONE_ORE: RedstoneOre,
                self.GLOWING_REDSTONE_ORE: GlowingRedstoneOre,
                self.REDSTONE_TORCH: RedstoneTorch,
                self.LIT_REDSTONE_TORCH: LitRedstoneTorch,
                self.STONE_BUTTON: StoneButton,
                self.SNOW_LAYER: SnowLayer,
                self.ICE: Ice,
                self.SNOW_BLOCK: Snow,
                self.CACTUS: Cactus,
                self.CLAY_BLOCK: Clay,
                self.SUGARCANE_BLOCK: Sugarcane,
                self.FENCE: Fence,
                self.PUMPKIN: Pumpkin,
                self.NETHERRACK: Netherrack,
                self.SOUL_SAND: SoulSand,
                self.GLOWSTONE_BLOCK: Glowstone,
                self.LIT_PUMPKIN: LitPumpkin,
                self.CAKE_BLOCK: Cake,
                self.TRAPDOOR: Trapdoor,
                self.STONE_BRICKS: StoneBricks,
                self.IRON_BARS: IronBars,
                self.GLASS_PANE: GlassPane,
                self.MELON_BLOCK: Melon,
                self.PUMPKIN_STEM: PumpkinStem,
                self.MELON_STEM: MelonStem,
                self.VINE: Vine,
                self.FENCE_GATE: FenceGate,
                self.BRICK_STAIRS: BrickStairs,
                self.STONE_BRICK_STAIRS: StoneBrickStairs,
                self.MYCELIUM: Mycelium,
                self.WATER_LILY: WaterLily,
                self.NETHER_BRICKS: NetherBrick,
                self.NETHER_BRICK_FENCE: NetherBrickFence,
                self.NETHER_BRICKS_STAIRS: NetherBrickStairs,
                self.ENCHANTING_TABLE: EnchantingTable,
                self.BREWING_STAND_BLOCK: BrewingStand,
                self.END_PORTAL: EndPortal,
                self.END_PORTAL_FRAME: EndPortalFrame,
                self.END_STONE: EndStone,
                self.END_STONE_BRICKS: EndStoneBricks,
                self.REDSTONE_LAMP: RedstoneLamp,
                self.LIT_REDSTONE_LAMP: LitRedstoneLamp,
                self.SANDSTONE_STAIRS: SandstoneStairs,
                self.EMERALD_ORE: EmeraldOre,
                self.ENDER_CHEST: EnderChest,
                self.TRIPWIRE_HOOK: TripwireHook,
                self.TRIPWIRE: Tripwire,
                self.EMERALD_BLOCK: Emerald,
                self.SPRUCE_WOOD_STAIRS: SpruceWoodStairs,
                self.BIRCH_WOOD_STAIRS: BirchWoodStairs,
                self.JUNGLE_WOOD_STAIRS: JungleWoodStairs,
                self.BEACON: Beacon,
                self.STONE_WALL: StoneWall,
                self.FLOWER_POT_BLOCK: FlowerPot,
                self.CARROT_BLOCK: Carrot,
                self.POTATO_BLOCK: Potato,
                self.WOODEN_BUTTON: WoodenButton,
                self.MOB_HEAD_BLOCK: MobHead,
                self.ANVIL: Anvil,
                self.TRAPPED_CHEST: TrappedChest,
                self.WEIGHTED_PRESSURE_PLATE_LIGHT: WeightedPressurePlateLight,
                self.WEIGHTED_PRESSURE_PLATE_HEAVY: WeightedPressurePlateHeavy,
                self.DAYLIGHT_SENSOR: DaylightSensor,
                self.REDSTONE_BLOCK: Redstone,
                self.COMMAND_BLOCK: CommandBlock,
                self.QUARTZ_BLOCK: Quartz,
                self.QUARTZ_STAIRS: QuartzStairs,
                self.DOUBLE_WOOD_SLAB: DoubleWoodSlab,
                self.WOOD_SLAB: WoodSlab,
                self.STAINED_CLAY: StainedClay,
                self.LEAVES2: Leaves2,
                self.WOOD2: Wood2,
                self.ACACIA_WOOD_STAIRS: AcaciaWoodStairs,
                self.DARK_OAK_WOOD_STAIRS: DarkOakWoodStairs,
                self.PRISMARINE: Prismarine,
                self.SEA_LANTERN: SeaLantern,
                self.IRON_TRAPDOOR: IronTrapdoor,
                self.HAY_BALE: HayBale,
                self.CARPET: Carpet,
                self.HARDENED_CLAY: HardenedClay,
                self.COAL_BLOCK: Coal,
                self.PACKED_ICE: PackedIce,
                self.DOUBLE_PLANT: DoublePlant,
                self.FENCE_GATE_SPRUCE: FenceGateSpruce,
                self.FENCE_GATE_BIRCH: FenceGateBirch,
                self.FENCE_GATE_JUNGLE: FenceGateJungle,
                self.FENCE_GATE_DARK_OAK: FenceGateDarkOak,
                self.FENCE_GATE_ACACIA: FenceGateAcacia,
                self.ITEM_FRAME_BLOCK: ItemFrame,
                self.GRASS_PATH: GrassPath,
                self.PODZOL: Podzol,
                self.BEETROOT_BLOCK: Beetroot,
                self.STONECUTTER: Stonecutter,
                self.GLOWING_OBSIDIAN: GlowingObsidian,
                self.HOPPER_BLOCK: Hopper,
                self.DRAGON_EGG: DragonEgg,
                self.CHORUS_FLOWER: ChorusFlower,
                self.CHORUS_PLANT: ChorusPlant,
                self.INVISIBLE_BEDROCK: InvisibleBedrock
            }

            for id, clas in list:
                if clas is not None:
                    block = clas()

                    for data in range(17):
                        self.fullList[(id << 4) | data] = clas(data)

                    self.solid[id] = block.isSolid()
                    self.transparent[id] = block.isTransparent()
                    self.hardness[id] = block.getHardness()
                    self.light[id] = block.getLightLevel()
                    if block.isSolid():
                        if block.isTransparent():
                            if isinstance(block, Liquid) or isinstance(block, Ice):
                                self.lightFilter[id] = 2
                            else:
                                self.lightFilter[id] = 1
                        else:
                            self.lightFilter[id] = 15
                    else:
                        self.lightFilter[id] = 1
                else:
                    self.lightFilter[id] = 1
                    for data in range(16):
                        self.fullList.append({(id << 4) | data: UnknownBlock(id, data)})

    def get(self, id, meta=0, pos: Position = None):
        try:
            block = self.list[id]
            if block is not None:
                block = block(meta)
            else:
                block = UnknownBlock(id, meta)
        except RuntimeError as e:
            block = UnknownBlock(id, meta)

        if pos is not None:
            block.x = pos.x
            block.y = pos.y
            block.z = pos.z
            block.level = pos.level

    def __init__(self, id, meta=0):
        super(Block, self).__init__()
        self.id = int(id)
        self.meta = int(meta)

    def place(self, item: Item, block: Block, target: Block, face, fx, fy, fz, player: Player = None):
        return self.getLevel().setBlock(self, self, True, True)

    def isBreakable(self, item: Item):
        return True

    def onBreak(self, item: Item):
        return self.getLevel().setBlock(self, Air, True, True)

    def onUpdate(self, type):
        return False

    def onActivate(self, item: Item, player: Player = None):
        return False

    def getHardness(self):
        return 10

    def getResistance(self):
        return self.getHardness() * 5

    def getToolType(self):
        return Tool.TYPE_NONE

    def getFrictionFactor(self):
        return 0.6

    def getLightLevel(self):
        return 0

    def canBePlaced(self):
        return True

    def canBeReplaced(self):
        return False

    def isTransparent(self):
        return False

    def isSolid(self):
        return True

    def canBeFlowedInto(self):
        return False

    def canBeActivated(self):
        return False

    def hasEntityCollision(self):
        return False

    def canPassThrough(self):
        return False

    def getName(self):
        return "Unknown"

    def getId(self):
        return self.id

    def addVelocityToEntity(self, entity: Entity, vector: Vector3):
        pass

    def getDamage(self):
        return self.meta

    def setDamage(self, meta):
        self.meta = meta & 0x0f

    def position(self, v: Position):
        self.x = int(v.x)
        self.y = int(v.y)
        self.z = int(v.z)
        self.level = v.level
        self.boundingBox = None

    def getDrops(self, item: Item):
        if not isset(self.list[self.getId()]):
            return []
        else:
            return [
                [self.getId(), self.getDamage(), 1],
            ]

    def getBreakTime(self, item: Item):
        base = self.getHardness() * 1.5
        if self.canBeBrokenWith(item):
            if self.getToolType() == Tool.TYPE_SHEARS and item.isShears():
                base /= 15
