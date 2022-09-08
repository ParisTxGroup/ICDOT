# How this works

This website can be used to upload and manage transplant data.

Information is organized using the following objects: `Transplant`,
`Biopsy`, `Histology`, `SequencingData`.

**Import / Export** is possible for each of the above in `json`, `csv`, or `xlsx` formats.

## References

Fields names ending in `_ref` indicate references.

On this website references are identifiers that are specific to the user
that is uploading the data. This website does not make any assumptions
about references except that they are strings.

## How things are identified

- `Transplant` entries are identified by `transplant_date`, `donor_ref` and `recipient_ref`.
- `Biopsy` entries are identified by a `Transplant` and a `biopsy_date`.
- `Histology` entries are identified by a `Biopsy` and a `histology_date`.
- `SequencingData` entries are identified by a `Biopsy` and a `sequencing_date`.

When importing or exporting data the identifying fields will be
included recursively. For example, because of how it is identified, a
`Histology` will always have the following fields: `histology_date`,
`biopsy_date`, `transplant_date`, `donor_ref` and `recipient_ref`.
That's because it is including the identifying fields of its biopsy
and the related transplant.

## How file uploads work


`SequencingData` can include an atoutached file (RCC data). When
importing data from `xlsx` files or `json` you can not directly upload
the associated files. Instead what you can do is:

  1. Create a new `FileUploadBatch` with all the associated files. The
     file names should be unique.
  2. When importing `SequencingData`, specify `file_ref` with the name
     of the file.

It is also possible to create the FileUploadBatch after having already
uploaded the data. The file names still need to match the `file_ref`.
