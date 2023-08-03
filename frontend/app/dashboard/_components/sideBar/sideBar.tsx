import { Box, Drawer, List, Toolbar } from "@mui/material";
import AssignmentTurnedInIcon from "@mui/icons-material/AssignmentTurnedIn";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import PlaceIcon from "@mui/icons-material/Place";
import StorageIcon from "@mui/icons-material/Storage";
import SideBarItem from "./sideBarItem";

const drawerWidth = 240;

export default function SideBar() {
  let sideBarItems = [
    { title: "Identity Providers", icon: <PeopleAltIcon />, link: "/identity_providers" },
    { title: "Locations", icon: <PlaceIcon />, link: "/locations" },
    { title: "Providers", icon: <StorageIcon />, link: "/providers" },
    { title: "SLAs", icon: <AssignmentTurnedInIcon />, link: "/slas" },
  ];
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: drawerWidth,
          boxSizing: "border-box",
        },
      }}
    >
      <Toolbar />
      <Box sx={{ overflow: "auto" }}>
        <List>
          {sideBarItems.map((item, index) => (
            <SideBarItem key={index} item={item} />
          ))}
        </List>
      </Box>
    </Drawer>
  );
}
