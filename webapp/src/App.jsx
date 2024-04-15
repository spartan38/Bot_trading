import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from '@mui/material/CssBaseline';
import MyDrawer from "./components/MyDrawer";
import { BrowserRouter as Router } from "react-router-dom";

const App = () => {
  const darkTheme = createTheme({
    palette: {
      mode: "dark", //default theme
    },
  });

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <MyDrawer />
      </Router>
    </ThemeProvider>
  );
};

export default App;
