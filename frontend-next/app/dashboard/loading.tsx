import { Grid } from "@mui/material";
import LoadingCard from "./_components/card/loading";

export default function Loading() {
  return (
    <Grid container spacing={2}>
      {[1, 2, 3].map((item) => (
        <Grid item xs={4}>
          <LoadingCard key={item} />
        </Grid>
      ))}
    </Grid>
  );
}
