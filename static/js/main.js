import jss from "jss";
import preset from "jss-preset-default";

jss.setup(preset());

const styles = {
  wrapper: {
    padding: 40,
    background: "#68c3df",
    textAlign: "center"
  },
  title: {
    font: {
      size: 40,
      weight: 900
    },
    color: "#FFFFFF"
  },
  link: {
    color: "#FFFFFF",
    "&:hover": {
      opacity: 0.5
    }
  }
};

const { classes } = jss.createStyleSheet(styles).attach();

document.body.innerHTML = `
  <div class="${classes.wrapper}">
    <h1 class="${classes.title}">Hello JSS!</h1>
    <a
      class=${classes.link}
      href="http://cssinjs.org/"
      traget="_blank"
    >
      See docs
    </a>
  </div>
`;
