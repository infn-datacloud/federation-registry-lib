import { Grid, Typography } from "@mui/material";
import SLACard from "./slaCard";
import UserGroupCard from "./userGroupCard";
import ProjectCard from "./projectCard";
import { SLA } from "../_lib/dbTypes";

export default function Skeleton({ item }: { item: SLA }) {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h3" align="center">
          SLA
        </Typography>
      </Grid>
      <Grid item xs={12} lg={6}>
        <SLACard item={item} />
      </Grid>
      <Grid item xs={12} lg={6}>
        <UserGroupCard item={item.user_group} />
      </Grid>
      <Grid item xs={12} lg={6}>
        <ProjectCard item={item.project} />
      </Grid>
    </Grid>
  );
}
