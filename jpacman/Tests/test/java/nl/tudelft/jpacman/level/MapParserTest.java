package nl.tudelft.jpacman.level;

import nl.tudelft.jpacman.board.BoardFactory;
import nl.tudelft.jpacman.npc.ghost.GhostFactory;
import nl.tudelft.jpacman.sprite.PacManSprites;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Test class for MapParser.
 * @author Angad Bhatti
 */
public class MapParserTest {

    private static final PacManSprites SPRITE_STORE = new PacManSprites();
    private final BoardFactory BOARD_FACTORY = new BoardFactory(SPRITE_STORE);
    private final GhostFactory GHOST_FACTORY = new GhostFactory(SPRITE_STORE);
    private final LevelFactory LEVEL_FACTORY = new LevelFactory(SPRITE_STORE, GHOST_FACTORY, null);
    private final MapParser MAP_PARSER = new MapParser(LEVEL_FACTORY, BOARD_FACTORY);

    @Test
    void testParseMap() {
        List<String> testMap = Arrays.asList(
            "#####",
            "#...#",
            "#G P#",
            "#...#",
            "#####"
        );

        Level level = MAP_PARSER.parseMap(testMap);
        assertThat(level).isNotNull();
    }
}
