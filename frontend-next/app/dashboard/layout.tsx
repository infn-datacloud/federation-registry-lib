import { Box, CssBaseline, Toolbar } from "@mui/material";
import TitleBar from "./_components/titleBar";
import SideBar from "./_components/sideBar/sideBar";

export default function DashboardLayout({
  children, // will be a page or nested layout
}: {
  children: React.ReactNode;
}) {
  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <TitleBar />
      <SideBar />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}
