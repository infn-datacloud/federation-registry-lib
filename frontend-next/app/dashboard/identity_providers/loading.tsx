import { Grid } from "@mui/material";
import LoadingCard from "../_components/card/loading";

export default function Loading() {
  const cards = ["1", "2", "3"];
  return (
    <Grid container spacing={2}>
      {cards.map((item, index) => (
        <Grid item key={index} xs={4}>
          <LoadingCard key={item} />
        </Grid>
      ))}
    </Grid>
  );
}
