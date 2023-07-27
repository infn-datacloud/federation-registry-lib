import {
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import Link from "next/link";
import { SideBarItem } from "../../_lib/uiTypes";

export default function SideBarItemLink({ item }: { item: SideBarItem }) {
  return (
    <Link href={`/dashboard/${item.link}`}>
      <ListItem disablePadding>
        <ListItemButton>
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText primary={item.title} />
        </ListItemButton>
      </ListItem>
    </Link>
  );
}
