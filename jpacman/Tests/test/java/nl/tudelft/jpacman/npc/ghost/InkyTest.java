package nl.tudelft.jpacman.npc.ghost;

import nl.tudelft.jpacman.sprite.PacManSprites;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Test class for Inky.
 * @author Angad Bhatti
 */
public class InkyTest {

    private static final PacManSprites SPRITE_STORE = new PacManSprites();

    private final GhostFactory ghostFactory = new GhostFactory(SPRITE_STORE);

    private final Inky inky = (Inky) ghostFactory.createInky();

    /**
     * Test if Inky was created.
     */
    @Test
    void inkyIsNotNull() {
        assertThat(inky).isNotNull();
    }
}
