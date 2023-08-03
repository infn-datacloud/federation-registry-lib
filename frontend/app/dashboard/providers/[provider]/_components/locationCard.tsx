import { LocationBase } from "@/app/dashboard/_lib/dbTypes";
import { Box, Card, CardContent, CardHeader, Typography } from "@mui/material";

export default function LocationCard({ item }: { item?: LocationBase }) {
  return (
    <Card>
      <CardHeader title="Location" />
      <CardContent>
        {item ? (
          <Box>
            <Typography>{item.name}</Typography>
            <Typography>{item.country}</Typography>
            <Typography>{item.latitude}</Typography>
            <Typography>{item.longitude}</Typography>
          </Box>
        ) : (
          "Location not defined"
        )}
      </CardContent>
    </Card>
  );
}
