import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import { Provider } from "../../_lib/dbTypes";

export default function ProvidersTable({
  items,
  page,
  rowsPerPage,
}: {
  page: number;
  rowsPerPage: number;
  items: Provider[];
}) {
  return (
    <Table sx={{ minWidth: 650 }}>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>Public/Private</TableCell>
          <TableCell>Support emails</TableCell>
          <TableCell>Communication Name</TableCell>
          <TableCell>Communication Protocol</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {items
          .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
          .map((item, index) => (
            <TableRow key={index}>
              <TableCell component="th" scope="row">
                {item.name}
              </TableCell>
              <TableCell>{item.is_public ? "Public" : "Private"}</TableCell>
              <TableCell>{item.support_emails.join(", ")}</TableCell>
              <TableCell>{item.relationship?.idp_name}</TableCell>
              <TableCell>{item.relationship?.protocol}</TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}
